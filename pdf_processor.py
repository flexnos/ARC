"""
PDF processing module for Answer Evaluation System.
Handles text extraction, OCR, and answer parsing.
"""

import re
import io
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import numpy as np

from config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


@dataclass
class ExtractedQuestion:
    """Represents an extracted question."""
    number: int
    text: str
    marks: int


@dataclass
class ParsedAnswer:
    """Represents a parsed student answer."""
    question_number: int
    text: str
    confidence: float = 1.0


class PDFTextExtractor:
    """Extract text from PDF files."""
    
    @staticmethod
    def extract_text(pdf_bytes: bytes) -> Dict[int, str]:
        """Extract text from PDF pages."""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            pages_text = {}
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                pages_text[page_num + 1] = text
            
            doc.close()
            return pages_text
            
        except Exception as e:
            logger.error(f"PDF text extraction error: {e}")
            raise PDFProcessingError(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_images(pdf_bytes: bytes, dpi: int = 200) -> Dict[int, List[Image.Image]]:
        """Extract images from PDF pages for OCR."""
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            pages_images = {}
            
            zoom = dpi / 72  # Convert DPI to zoom factor
            mat = fitz.Matrix(zoom, zoom)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                pages_images[page_num + 1] = [image]
            
            doc.close()
            return pages_images
            
        except Exception as e:
            logger.error(f"PDF image extraction error: {e}")
            raise PDFProcessingError(f"Failed to extract images from PDF: {str(e)}")


class OCRProcessor:
    """Process images with OCR."""
    
    PSM_MODES = [6, 3, 4, 11]  # Page segmentation modes to try
    
    @classmethod
    def preprocess_image(cls, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results."""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too small
            min_width = 1500
            if image.size[0] < min_width:
                ratio = min_width / image.size[0]
                new_size = (min_width, int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to grayscale
            gray = image.convert('L')
            
            # Apply median filter to reduce noise
            for _ in range(2):
                gray = gray.filter(ImageFilter.MedianFilter(size=3))
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(gray)
            contrasted = enhancer.enhance(2.5)
            
            # Enhance sharpness
            sharpness_enhancer = ImageEnhance.Sharpness(contrasted)
            sharpened = sharpness_enhancer.enhance(2.0)
            
            # Auto contrast
            thresholded = ImageOps.autocontrast(sharpened, cutoff=2)
            
            # Slight brightness increase
            brightness_enhancer = ImageEnhance.Brightness(thresholded)
            final_image = brightness_enhancer.enhance(1.2)
            
            return final_image
            
        except Exception as e:
            logger.error(f"Image preprocessing error: {e}")
            # Return original image as fallback
            return image.convert('L') if image.mode != 'L' else image
    
    @classmethod
    def perform_ocr(cls, image: Image.Image, configs: List[str] = None) -> Tuple[str, float]:
        """Perform OCR with multiple configurations and return best result."""
        if configs is None:
            configs = [f'--psm {psm} --oem 3' for psm in cls.PSM_MODES]
        
        preprocessed = cls.preprocess_image(image)
        best_text = ""
        best_confidence = 0.0
        
        for config in configs:
            try:
                # Extract text
                extracted = pytesseract.image_to_string(preprocessed, config=config)
                
                # Get confidence data
                try:
                    data = pytesseract.image_to_data(
                        preprocessed, 
                        config=config, 
                        output_type=pytesseract.Output.DICT
                    )
                    confidences = [int(conf) for conf in data['conf'] if conf != '-1']
                    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                except Exception:
                    avg_confidence = 50  # Default if confidence extraction fails
                
                # Score based on confidence and text length
                score = (avg_confidence * 0.6) + (min(len(extracted), 1000) / 1000 * 40)
                
                if score > best_confidence and len(extracted.strip()) > 10:
                    best_text = extracted
                    best_confidence = score
                    
            except Exception as e:
                logger.warning(f"OCR with config '{config}' failed: {e}")
                continue
        
        return best_text, best_confidence / 100  # Normalize to 0-1
    
    @classmethod
    def detect_diagram(cls, image: Image.Image) -> bool:
        """Detect if image contains a diagram."""
        try:
            # Try OpenCV first
            import cv2
            cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(
                edges, rho=1, theta=np.pi/180, threshold=50,
                minLineLength=30, maxLineGap=10
            )
            line_count = len(lines) if lines is not None else 0
            edge_density = (edges > 0).sum() / edges.size
            
            return (line_count >= 15) or (edge_density >= 0.04)
            
        except ImportError:
            # Fallback to PIL
            try:
                edge_img = image.convert("L").filter(ImageFilter.FIND_EDGES)
                bw = edge_img.point(lambda p: 255 if p > 30 else 0)
                pixels = list(bw.getdata())
                dark = sum(1 for p in pixels if p == 0)
                edge_density = dark / len(pixels)
                return edge_density >= 0.04
            except Exception as e:
                logger.warning(f"Diagram detection failed: {e}")
                return False


class TextCleaner:
    """Clean and normalize extracted text."""
    
    CHEMICAL_PATTERNS = [
        (r'(?i)c\s*o\s*2', 'CO2'),
        (r'(?i)h\s*2\s*o', 'H2O'),
        (r'(?i)o\s*2', 'O2'),
        (r'(?i)c\s*o', 'CO'),
        (r'(?i)n\s*2', 'N2'),
        (r'(?i)h\s*2', 'H2'),
    ]
    
    @classmethod
    def clean(cls, text: str) -> str:
        """Clean extracted text."""
        if not text:
            return ""
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix chemical formulas
        for pattern, replacement in cls.CHEMICAL_PATTERNS:
            text = re.sub(pattern, replacement, text)
        
        # Fix punctuation spacing
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'([.,!?;:])\s*', r'\1 ', text)
        
        # Capitalize sentence starts
        sentences = re.split(r'([.!?])\s*', text)
        cleaned_sentences = []
        for i, part in enumerate(sentences):
            if part and part not in '.!?':
                if i == 0 or (i > 0 and sentences[i-1] in '.!?'):
                    part = part[0].upper() + part[1:] if len(part) > 1 else part.upper()
            cleaned_sentences.append(part)
        
        text = ''.join(cleaned_sentences)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()


class AnswerParser:
    """Parse answers from extracted text."""
    
    QUESTION_PATTERNS = [
        r'(?i)(?:q(?:uestion)?\.?\s*(\d+))[.):\s]+(.+)',
        r'(?i)(\d+)[.):\s]+(.+)',
    ]
    
    MARKS_PATTERNS = [
        r'(?i)(?:\(|\[)(\d+)\s*(?:marks?|m)(?:\)|\])',
        r'(?i)marks?\s*[:=]?\s*(\d+)',
    ]
    
    @classmethod
    def parse_questions(cls, text: str) -> List[ExtractedQuestion]:
        """Extract questions and marks from question paper text."""
        questions = []
        lines = text.split('\n')
        current_q = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to match question pattern
            q_match = None
            for pattern in cls.QUESTION_PATTERNS:
                q_match = re.match(pattern, line)
                if q_match:
                    break
            
            # Try to match marks pattern
            marks = 5  # default
            for pattern in cls.MARKS_PATTERNS:
                marks_match = re.search(pattern, line)
                if marks_match:
                    marks = int(marks_match.group(1))
                    break
            
            if q_match:
                if current_q:
                    questions.append(current_q)
                current_q = ExtractedQuestion(
                    number=int(q_match.group(1)),
                    text=q_match.group(2).strip(),
                    marks=marks
                )
            elif current_q and line:
                # Append to current question text
                current_q.text += ' ' + line
        
        if current_q:
            questions.append(current_q)
        
        return questions
    
    @classmethod
    def extract_answer_for_question(
        cls,
        all_text: str,
        question_num: int,
        next_question_num: Optional[int] = None
    ) -> str:
        """Extract student answer for specific question number."""
        # Build end pattern
        if next_question_num:
            pattern_end = fr'(?:q\.?\s*{next_question_num}|question\s*{next_question_num}|{next_question_num}\.)'
        else:
            pattern_end = r'\Z'
        
        # Try different patterns
        patterns = [
            rf'(?i)q\.?\s*{question_num}[\s:.\)]+(.+?)(?={pattern_end})',
            rf'(?i)question\s*{question_num}[\s:.\)]+(.+?)(?={pattern_end})',
            rf'(?i){question_num}\.?\s+(.+?)(?={pattern_end})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, all_text, re.DOTALL)
            if match:
                answer = match.group(1).strip()
                return TextCleaner.clean(answer)
        
        # Fallback: line-by-line parsing
        lines = all_text.split('\n')
        in_answer = False
        answer_lines = []
        
        for line in lines:
            if re.search(rf'(?i)q\.?\s*{question_num}[\s:.\)]', line):
                in_answer = True
                continue
            if next_question_num and re.search(rf'(?i)q\.?\s*{next_question_num}[\s:.\)]', line):
                break
            if in_answer:
                answer_lines.append(line)
        
        return TextCleaner.clean(' '.join(answer_lines))
    
    @classmethod
    def parse_reference_answers(
        cls,
        ref_text: str,
        questions: List[ExtractedQuestion]
    ) -> Dict[int, str]:
        """Parse reference answers for given questions."""
        ref_answers = {}
        
        for i, q in enumerate(questions):
            q_num = q.number
            next_q_num = questions[i + 1].number if i + 1 < len(questions) else None
            
            patterns = [
                rf'(?i)q\.?\s*{q_num}[\s:.\)]+(.+?)(?=q\.?\s*{q_num + 1}|\Z)',
                rf'(?i)question\s*{q_num}[\s:.\)]+(.+?)(?=question\s*{q_num + 1}|\Z)',
                rf'(?i){q_num}[.):\s]+(.+?)(?={q_num + 1}[.):\s]|\Z)',
            ]
            
            ref_ans = ""
            for pattern in patterns:
                match = re.search(pattern, ref_text, re.DOTALL)
                if match:
                    ref_ans = TextCleaner.clean(match.group(1))
                    break
            
            ref_answers[q_num] = ref_ans if ref_ans else "Reference answer not found"
        
        return ref_answers


class PDFProcessingError(Exception):
    """Custom exception for PDF processing errors."""
    pass


class PDFProcessor:
    """Main PDF processing class."""
    
    def __init__(self):
        self.text_extractor = PDFTextExtractor()
        self.ocr_processor = OCRProcessor()
        self.text_cleaner = TextCleaner()
        self.answer_parser = AnswerParser()
    
    def process_answer_sheet(
        self,
        pdf_bytes: bytes,
        use_ocr_threshold: int = None
    ) -> str:
        """Process student answer sheet, using OCR if needed."""
        use_ocr_threshold = use_ocr_threshold or settings.OCR_MIN_TEXT_LENGTH
        
        # Extract text
        pages = self.text_extractor.extract_text(pdf_bytes)
        total_text = ' '.join(pages.values())
        
        # Use OCR if text is too sparse
        if len(total_text.strip()) < use_ocr_threshold:
            logger.info("Text extraction yielded sparse results, running OCR...")
            images = self.text_extractor.extract_images(pdf_bytes)
            
            ocr_texts = []
            for page_num, page_images in images.items():
                for img in page_images:
                    text, confidence = self.ocr_processor.perform_ocr(img)
                    if text.strip():
                        ocr_texts.append(text)
            
            total_text = ' '.join(ocr_texts)
            logger.info(f"OCR extracted {len(total_text)} characters")
        
        return self.text_cleaner.clean(total_text)
    
    def process_question_paper(self, pdf_bytes: bytes) -> List[ExtractedQuestion]:
        """Process question paper and extract questions."""
        pages = self.text_extractor.extract_text(pdf_bytes)
        text = ' '.join(pages.values())
        return self.answer_parser.parse_questions(text)
    
    def process_reference_answers(
        self,
        pdf_bytes: bytes,
        questions: List[ExtractedQuestion]
    ) -> Dict[int, str]:
        """Process reference answers PDF."""
        pages = self.text_extractor.extract_text(pdf_bytes)
        text = ' '.join(pages.values())
        return self.answer_parser.parse_reference_answers(text, questions)


# Convenience function
def get_pdf_processor() -> PDFProcessor:
    """Get PDF processor instance."""
    return PDFProcessor()
