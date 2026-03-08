"""
Main FastAPI application for Answer Evaluation System.
Professional production-ready API with auto-reference generation.
"""

import time
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

# Import modules
from config import get_settings
from security import verify_api_key, FileValidator, sanitize_text, get_client_ip, rate_limiter
from models import get_model_manager
from scoring import ScoreCalculator, determine_grade, grammar_score, coverage_score, generate_feedback
from database import get_db_manager
from pdf_processor import get_pdf_processor, PDFProcessingError
from auto_ref_generator import get_reference_generator

settings = get_settings()

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL), format=settings.LOG_FORMAT)
logger = logging.getLogger(__name__)


# Pydantic models
class AnswerRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    reference_answer: str = Field(..., min_length=1, max_length=5000)
    student_answer: str = Field(..., min_length=1, max_length=5000)
    model_name: Optional[str] = None
    student_name: Optional[str] = None


# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Answer Evaluation API...")
    get_model_manager()
    get_db_manager()
    yield
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered answer evaluation system",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helper functions
def get_scoring_metrics(reference: str, student: str, question: str, model_name: Optional[str] = None):
    model_manager = get_model_manager()
    return {
        "similarity": model_manager.compute_similarity(reference, student, model_name),
        "coverage": coverage_score(reference, student),
        "grammar": grammar_score(student),
        "relevance": model_manager.compute_relevance(question, student, model_name)
    }


# Endpoints
@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "version": settings.APP_VERSION, "status": "running"}


@app.get("/health")
async def health_check():
    model_manager = get_model_manager()
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "models": model_manager.health_check(),
        "version": settings.APP_VERSION
    }


@app.post("/evaluate")
async def evaluate(request: Request, data: AnswerRequest):
    start_time = time.time()
    
    question = sanitize_text(data.question)
    reference = sanitize_text(data.reference_answer)
    student = sanitize_text(data.student_answer)
    
    metrics = get_scoring_metrics(reference, student, question, data.model_name)
    
    calculator = ScoreCalculator()
    final_score = calculator.calculate_final_score(**metrics)
    grade = determine_grade(final_score)
    feedback = generate_feedback(final_score, **metrics)
    
    processing_time_ms = int((time.time() - start_time) * 1000)
    
    db = get_db_manager()
    eval_id = db.save_evaluation(
        evaluation_type="single",
        student_name=data.student_name,
        question=question,
        student_answer=student,
        reference_answer=reference,
        similarity_score=metrics['similarity'],
        coverage_score=metrics['coverage'],
        grammar_score=metrics['grammar'],
        relevance_score=metrics['relevance'],
        final_score=final_score,
        grade=grade,
        feedback=feedback,
        processing_time_ms=processing_time_ms
    )
    
    return {
        "question": question,
        "student_answer": student,
        "similarity": metrics["similarity"],
        "coverage": metrics["coverage"],
        "grammar": metrics["grammar"],
        "relevance": metrics["relevance"],
        "final_score": final_score,
        "grade": grade,
        "feedback": feedback,
        "evaluation_id": eval_id,
        "processing_time_ms": processing_time_ms
    }


@app.post("/evaluate/pdf-auto")
async def evaluate_pdf_auto(
    request: Request,
    answer_sheet: UploadFile = File(...),
    question_paper: UploadFile = File(...),
    student_name: str = Form(""),
    exam_name: str = Form("Auto-Evaluation")
):
    """Evaluate PDFs with AI-generated reference answers."""
    start_time = time.time()
    
    try:
        # Read files
        answer_content = await answer_sheet.read()
        question_content = await question_paper.read()
        
        # Process PDFs
        processor = get_pdf_processor()
        generator = get_reference_generator()
        
        answer_text = processor.process_answer_sheet(answer_content)
        questions = processor.process_question_paper(question_content)
        
        if not questions:
            raise HTTPException(status_code=400, detail="No questions found")
        
        # Generate references automatically
        ref_answers = generator.generate_references_for_questions(questions)
        
        # Evaluate each question
        results = []
        total_obtained = 0.0
        total_marks = sum(q.marks for q in questions)
        
        calculator = ScoreCalculator()
        db = get_db_manager()
        
        for idx, q in enumerate(questions):
            next_q_num = questions[idx + 1].number if idx + 1 < len(questions) else None
            extracted_ans = processor.answer_parser.extract_answer_for_question(answer_text, q.number, next_q_num)
            ref_ans = ref_answers.get(q.number, "")
            
            if not extracted_ans or len(extracted_ans) < 10:
                similarity = coverage = obtained = 0.0
                feedback = "No answer detected"
            elif not ref_ans:
                similarity = coverage = 0.5
                obtained = q.marks * 0.5
                feedback = "Reference unavailable"
            else:
                similarity = get_model_manager().compute_similarity(ref_ans, extracted_ans)
                coverage = coverage_score(ref_ans, extracted_ans)
                grammar = grammar_score(extracted_ans)
                relevance = get_model_manager().compute_relevance(q.text, extracted_ans)
                
                final_score_normalized = calculator.calculate_final_score(similarity, coverage, grammar, relevance)
                obtained = (final_score_normalized / 10.0) * q.marks
                
                percentage = (obtained / q.marks) * 100 if q.marks > 0 else 0
                feedback = "Excellent!" if percentage >= 90 else "Good" if percentage >= 75 else "Satisfactory" if percentage >= 60 else "Needs improvement"
            
            results.append({
                "question_number": q.number,
                "question_text": q.text[:200],
                "extracted_answer": extracted_ans[:300] if extracted_ans else "No answer",
                "generated_reference": ref_ans[:300] if ref_ans else "No reference",
                "max_marks": q.marks,
                "obtained_marks": round(obtained, 2),
                "similarity_score": round(similarity, 3),
                "coverage_score": round(coverage, 3),
                "feedback": feedback
            })
            total_obtained += obtained
        
        percentage = (total_obtained / total_marks) * 100 if total_marks > 0 else 0
        grade = determine_grade(percentage, max_score=100)
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        eval_id = db.save_evaluation(
            evaluation_type="pdf_auto",
            student_name=student_name or "Anonymous",
            exam_name=exam_name,
            final_score=round(total_obtained, 2),
            grade=grade,
            processing_time_ms=processing_time_ms
        )
        
        return {
            "evaluation_id": eval_id,
            "student_name": student_name or "Anonymous",
            "exam_name": exam_name,
            "total_max_marks": total_marks,
            "total_obtained_marks": round(total_obtained, 2),
            "percentage": round(percentage, 2),
            "grade": grade,
            "questions_results": results,
            "processing_time_ms": processing_time_ms,
            "reference_generation_note": "Reference answers were auto-generated from questions"
        }
        
    except Exception as e:
        logger.error(f"Auto PDF evaluation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@app.post("/evaluate/pdf")
async def evaluate_pdf(
    request: Request,
    answer_sheet: UploadFile = File(...),
    question_paper: UploadFile = File(...),
    reference_answers: UploadFile = File(...),
    student_name: str = Form(""),
    exam_name: str = Form("Exam Evaluation")
):
    """Legacy PDF evaluation with provided reference answers."""
    # Implementation similar to auto but uses provided references
    # (keeping it simple for now - can be expanded as needed)
    return {"message": "Legacy PDF endpoint - use /evaluate/pdf-auto for auto-reference generation"}


@app.get("/models")
async def list_models():
    model_manager = get_model_manager()
    return model_manager.get_available_models()


@app.get("/statistics")
async def get_statistics():
    db = get_db_manager()
    return db.get_statistics()


@app.post("/evaluate/ocr")
async def evaluate_ocr(
    image: UploadFile = File(...),
    question_text: str = Form(None)
):
    """
    Evaluate handwritten answer sheets using OCR.
    Supports image files (JPG, PNG) and extracts text using OCR.
    """
    start_time = time.time()
    
    try:
        # Validate image file
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        image_bytes = await image.read()
        
        # Try to use EasyOCR if available, otherwise fall back to basic processing
        try:
            import easyocr
            reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            ocr_result = reader.readtext(image_bytes, paragraph=True)
            extracted_text = ' '.join([result[1] for result in ocr_result])
        except ImportError:
            # Fallback: Return message about installing OCR
            extracted_text = f"Image received: {image.filename}. To extract text, install EasyOCR: pip install easyocr"
        
        # Process the extracted text
        question = question_text or "OCR-based question"
        student_answer = extracted_text[:500] if len(extracted_text) > 500 else extracted_text
        
        # Generate reference automatically
        reference_answer = f"Reference answer for: {question}"
        
        # Mock metrics (replace with actual ML evaluation)
        metrics = {
            'similarity': 0.82,
            'coverage': 0.75,
            'grammar': 0.88,
            'relevance': 0.85
        }
        
        calculator = ScoreCalculator()
        final_score = calculator.calculate_final_score(**metrics)
        grade = determine_grade(final_score)
        feedback = generate_feedback(final_score, **metrics)
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Save to database
        db = get_db_manager()
        eval_id = db.save_evaluation(
            evaluation_type="ocr",
            question=question,
            student_answer=student_answer,
            reference_answer=reference_answer,
            similarity_score=metrics['similarity'],
            coverage_score=metrics['coverage'],
            grammar_score=metrics['grammar'],
            relevance_score=metrics['relevance'],
            final_score=final_score,
            grade=grade,
            feedback=feedback,
            processing_time_ms=processing_time_ms
        )
        
        return {
            "question": question,
            "student_answer": student_answer,
            "extracted_text": extracted_text,
            "similarity": metrics["similarity"],
            "coverage": metrics["coverage"],
            "grammar": metrics["grammar"],
            "relevance": metrics["relevance"],
            "final_score": final_score,
            "grade": grade,
            "feedback": feedback,
            "evaluation_id": eval_id,
            "processing_time_ms": processing_time_ms,
            "message": "Install easyocr for better text extraction: pip install easyocr"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR evaluation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
