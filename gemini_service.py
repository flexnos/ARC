"""
Google Gemini LLM Integration for Answer Evaluation System.
Provides AI-powered reference answer generation and intelligent scoring.
Includes detailed logging and API usage tracking.
"""

import logging
from typing import Optional, Dict, Any
from config import get_settings

logger = logging.getLogger(__name__)


class GeminiService:
    """Service class for interacting with Gemini API."""
    
    def __init__(self):
        self.settings = get_settings()
        self.model = None
        self._initialized = False
        self._usage_count = 0  # Track API calls in this session
        
        # Only initialize if API key is provided
        if self.settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                
                # Configure the API key
                genai.configure(api_key=self.settings.GEMINI_API_KEY)
                
                # Initialize the model
                self.model = genai.GenerativeModel(self.settings.GEMINI_MODEL)
                self._initialized = True
                logger.info(f"✨ Gemini LLM initialized with model: {self.settings.GEMINI_MODEL}")
                logger.info(f"📊 Free tier limits: 60 requests/min, 1500 requests/day")
            except ImportError:
                logger.warning("google-generativeai package not installed. Install with: pip install google-generativeai")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini LLM: {e}. Falling back to heuristic-based generation.")
        else:
            logger.warning("⚠️  GEMINI_API_KEY not set. LLM features will be disabled.")
    
    def is_available(self) -> bool:
        """Check if Gemini LLM is available."""
        return self._initialized and self.model is not None
    
    def generate_reference_answer(self, question: str, max_length: int = 500) -> Optional[str]:
        """
        Generate a comprehensive reference answer using Gemini LLM.
        
        Args:
            question: The question text
            max_length: Maximum length of the generated answer
            
        Returns:
            Generated reference answer or None if LLM is unavailable
        """
        if not self.is_available():
            return None
        
        try:
            # Create a detailed prompt for generating a reference answer
            prompt = f"""You are an expert educational assistant. Your task is to generate a comprehensive, well-structured reference answer for the following question.

Question: {question}

Guidelines:
1. Provide a clear, accurate, and educationally appropriate answer
2. Include key concepts and important details that should be mentioned
3. Structure your answer logically (introduction, main points, conclusion)
4. Use academic language appropriate for student assessment
5. Keep the answer concise but comprehensive (around {max_length} characters)

Reference Answer:"""

            # Generate the response
            self._usage_count += 1
            logger.info(f"🚀 [Gemini API Call #{self._usage_count}] Generating reference answer...")
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': self.settings.LLM_TEMPERATURE,
                    'max_output_tokens': self.settings.LLM_MAX_TOKENS,
                }
            )
            
            # Extract and clean the generated text
            if response and response.text:
                generated_answer = response.text.strip()
                logger.info(f"✅ Gemini generated reference answer ({len(generated_answer)} chars) - Session usage: {self._usage_count} calls")
                return generated_answer
            else:
                logger.warning("❌ Gemini returned empty response")
                return None
                
        except Exception as e:
            logger.error(f"❌ Gemini reference generation error: {e}")
            return None
    
    def evaluate_answer_quality(
        self,
        question: str,
        reference_answer: str,
        student_answer: str
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate a student's answer using Gemini LLM for intelligent assessment.
        
        Args:
            question: The original question
            reference_answer: The ideal reference answer
            student_answer: The student's answer to evaluate
            
        Returns:
            Dictionary with evaluation metrics or None if LLM is unavailable
        """
        if not self.is_available():
            return None
        
        try:
            # Create evaluation prompt
            prompt = f"""You are an expert educational evaluator. Analyze and compare the following question, reference answer, and student answer.

Question: {question}

Reference Answer (Ideal):
{reference_answer}

Student Answer:
{student_answer}

Task: Evaluate the student's answer based on:
1. Content Coverage - What percentage of key concepts from the reference answer are present?
2. Accuracy - How factually correct is the information?
3. Completeness - Does the answer address all parts of the question?
4. Clarity - Is the answer well-organized and easy to understand?

Provide your evaluation in this exact JSON format:
{{
    "coverage_score": 0-100,
    "accuracy_score": 0-100,
    "completeness_score": 0-100,
    "clarity_score": 0-100,
    "overall_score": 0-100,
    "matched_concepts": ["list", "of", "concepts", "present"],
    "missing_concepts": ["list", "of", "concepts", "absent"],
    "feedback": "Detailed feedback for the student",
    "strengths": ["list", "of", "strengths"],
    "areas_for_improvement": ["list", "of", "improvements"]
}}

Evaluation:"""

            # Generate the evaluation
            self._usage_count += 1
            logger.info(f"🚀 [Gemini API Call #{self._usage_count}] Evaluating answer quality...")
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.2,  # Lower temperature for more consistent evaluations
                    'max_output_tokens': 800,
                }
            )
            
            if response and response.text:
                import json
                import re
                
                # Try to parse the JSON response
                try:
                    # Extract JSON from response (handle markdown code blocks)
                    json_match = re.search(r'\{[\s\S]*\}', response.text)
                    if json_match:
                        evaluation = json.loads(json_match.group())
                        logger.info(f"✅ Gemini successfully evaluated answer - Session usage: {self._usage_count} calls")
                        return evaluation
                    else:
                        logger.warning("❌ No JSON found in Gemini response")
                        return None
                except json.JSONDecodeError as e:
                    logger.error(f"❌ Failed to parse Gemini JSON response: {e}")
                    return None
            else:
                logger.warning("❌ Gemini returned empty evaluation")
                return None
                
        except Exception as e:
            logger.error(f"❌ Gemini evaluation error: {e}")
            return None
    
    def enhance_feedback(
        self,
        question: str,
        student_answer: str,
        base_feedback: str
    ) -> Optional[str]:
        """
        Use Gemini to enhance and elaborate on automated feedback.
        
        Args:
            question: The question being answered
            student_answer: The student's answer
            base_feedback: Basic feedback from traditional scoring
            
        Returns:
            Enhanced feedback or None if LLM is unavailable
        """
        if not self.is_available():
            return None
        
        try:
            prompt = f"""You are a helpful educational tutor. Enhance the following feedback for a student's answer.

Question: {question}

Student Answer: {student_answer}

Basic Feedback: {base_feedback}

Task: Make the feedback more constructive, encouraging, and specific. Include:
1. Specific examples from the student's answer
2. Clear explanations of what was done well
3. Actionable suggestions for improvement
4. Encouraging tone

Enhanced Feedback:"""

            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.4,
                    'max_output_tokens': 400,
                }
            )
            
            if response and response.text:
                enhanced = response.text.strip()
                self._usage_count += 1
                logger.info(f"✅ Gemini enhanced feedback ({len(enhanced)} chars) - Session usage: {self._usage_count} calls")
                return enhanced
            else:
                logger.warning("❌ Gemini returned empty feedback")
                return None
                
        except Exception as e:
            logger.error(f"❌ Gemini feedback enhancement error: {e}")
            return None


# Singleton instance
_gemini_service: Optional[GeminiService] = None


def get_gemini_service() -> GeminiService:
    """Get or create the Gemini service singleton."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
