"""
Scoring module for Answer Evaluation System.
Centralized scoring logic with configurable weights.
"""

import re
import logging
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

from fuzzywuzzy import fuzz

from config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


@dataclass
class ScoreResult:
    """Result of scoring an answer."""
    similarity: float
    coverage: float
    grammar: float
    relevance: float
    final_score: float
    grade: str
    feedback: str
    detailed_metrics: Dict
    cnn_score: Optional[float] = None  # Added for CNN scoring (optional with default)


class GradeCalculator:
    """Calculate letter grades from scores."""
    
    GRADE_SCALE = [
        (90, "A+"),
        (85, "A"),
        (80, "A-"),
        (75, "B+"),
        (70, "B"),
        (65, "B-"),
        (60, "C+"),
        (55, "C"),
        (50, "C-"),
        (40, "D"),
        (0, "F")
    ]
    
    @classmethod
    def from_percentage(cls, percentage: float) -> str:
        """Get grade from percentage (0-100)."""
        for threshold, grade in cls.GRADE_SCALE:
            if percentage >= threshold:
                return grade
        return "F"
    
    @classmethod
    def from_score(cls, score: float, max_score: float = 10.0) -> str:
        """Get grade from score (0-max_score)."""
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        return cls.from_percentage(percentage)


class GrammarScorer:
    """Score grammar quality of text."""
    
    @staticmethod
    def score(text: str) -> float:
        """Calculate grammar score (0-1)."""
        try:
            if not text or not isinstance(text, str):
                return 0.5
            
            text = text.strip()
            if not text:
                return 0.5
            
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if not sentences:
                return 0.5
            
            score = 1.0
            
            # Check capitalization
            capitalized = sum(1 for s in sentences if s and s[0].isupper())
            cap_ratio = capitalized / len(sentences)
            
            # Check ending punctuation
            has_ending_punct = text[-1] in '.!?' if text else False
            
            # Check sentence length
            words_per_sentence = [len(s.split()) for s in sentences]
            avg_words = sum(words_per_sentence) / len(words_per_sentence)
            
            # Penalty for very short or very long sentences
            length_penalty = 0
            if avg_words < 3:
                length_penalty = 0.3
            elif avg_words > 30:
                length_penalty = 0.2
            
            # Calculate final score
            score = (cap_ratio * 0.4) + (0.3 if has_ending_punct else 0) + max(0, 0.3 - length_penalty)
            
            # Additional checks for common issues
            # Check for repeated punctuation
            if re.search(r'[.]{2,}|[!]{2,}|[?]{2,}', text):
                score -= 0.1
            
            # Check for all caps words (shouting)
            words = text.split()
            caps_words = sum(1 for w in words if w.isupper() and len(w) > 1)
            if caps_words > len(words) * 0.3:
                score -= 0.1
            
            return round(max(0.0, min(1.0, score)), 3)
            
        except Exception as e:
            logger.error(f"Grammar scoring error: {e}")
            return 0.5


class CoverageScorer:
    """Score keyword coverage between reference and student answer."""
    
    @staticmethod
    def score(reference: str, student: str, threshold: int = 70) -> float:
        """Calculate fuzzy keyword coverage (0-1)."""
        try:
            if not reference or not student:
                return 0.0
            
            # Extract meaningful words (length > 2)
            ref_words = set(
                word.lower() for word in reference.split()
                if len(word) > 2 and word.isalnum()
            )
            student_words = set(
                word.lower() for word in student.split()
                if len(word) > 2 and word.isalnum()
            )
            
            if not ref_words:
                return 0.0
            
            matched = 0
            for ref_word in ref_words:
                # Check for exact match or fuzzy match
                for student_word in student_words:
                    if (
                        ref_word == student_word or
                        ref_word in student_word or
                        student_word in ref_word or
                        fuzz.ratio(ref_word, student_word) > threshold
                    ):
                        matched += 1
                        break
            
            return round(matched / len(ref_words), 3)
            
        except Exception as e:
            logger.error(f"Coverage scoring error: {e}")
            return 0.0


class FeedbackGenerator:
    """Generate feedback based on scores."""
    
    @staticmethod
    def generate(
        score: float,
        similarity: float,
        coverage: float,
        grammar: float,
        relevance: float,
        max_score: float = 10.0
    ) -> str:
        """Generate comprehensive feedback."""
        feedback_parts = []
        
        # Overall assessment
        percentage = (score / max_score) * 100
        if percentage >= 90:
            feedback_parts.append("Excellent answer! Outstanding comprehension and expression.")
        elif percentage >= 75:
            feedback_parts.append("Good answer with room for minor improvements.")
        elif percentage >= 60:
            feedback_parts.append("Satisfactory answer but needs improvement in key areas.")
        elif percentage >= 40:
            feedback_parts.append("Answer needs significant improvement.")
        else:
            feedback_parts.append("Answer requires substantial revision. Please review the topic.")
        
        # Specific suggestions
        suggestions = []
        
        if similarity < 0.6:
            suggestions.append("Include more concepts from the reference material.")
        
        if coverage < 0.5:
            suggestions.append("Cover more key terms and important points.")
        
        if grammar < 0.6:
            suggestions.append("Work on sentence structure, capitalization, and punctuation.")
        
        if relevance < 0.5:
            suggestions.append("Ensure your answer directly addresses the question asked.")
        
        if suggestions:
            feedback_parts.append("Suggestions: " + " ".join(suggestions))
        
        return " ".join(feedback_parts)


class ScoreCalculator:
    """Main scoring calculator."""
    
    def __init__(self, use_cnn: bool = False, cnn_weight: Optional[float] = None):
        self.weights = {
            'similarity': settings.WEIGHT_SIMILARITY,
            'coverage': settings.WEIGHT_COVERAGE,
            'grammar': settings.WEIGHT_GRAMMAR,
            'relevance': settings.WEIGHT_RELEVANCE
        }
        self.use_cnn = use_cnn
        self.cnn_weight = cnn_weight if cnn_weight is not None else settings.CNN_WEIGHT
        # Adjust weights if using CNN
        if use_cnn:
            # Reduce other weights proportionally to accommodate CNN
            scale_factor = 1.0 - self.cnn_weight
            self.weights['similarity'] *= scale_factor
            self.weights['coverage'] *= scale_factor
            self.weights['grammar'] *= scale_factor
            self.weights['relevance'] *= scale_factor
            self.weights['cnn'] = self.cnn_weight
    
    def calculate_final_score(
        self,
        similarity: float,
        coverage: float,
        grammar: float,
        relevance: float,
        cnn_score: Optional[float] = None
    ) -> float:
        """Calculate weighted final score (0-10)."""
        weighted_sum = (
            self.weights['similarity'] * similarity +
            self.weights['coverage'] * coverage +
            self.weights['grammar'] * grammar +
            self.weights['relevance'] * relevance
        )
        
        # Add CNN score if available and enabled
        if self.use_cnn and cnn_score is not None:
            weighted_sum += self.weights.get('cnn', 0) * cnn_score
        
        return round(weighted_sum * 10, 2)
    
    def calculate_with_bonus(
        self,
        similarity: float,
        coverage: float,
        grammar: float,
        relevance: float,
        cnn_score: Optional[float] = None,
        has_diagram: bool = False,
        diagram_bonus: float = 0.5,
        max_score: float = 10.0
    ) -> Tuple[float, float]:
        """Calculate score with optional diagram bonus."""
        base_score = self.calculate_final_score(similarity, coverage, grammar, relevance, cnn_score)
        
        if has_diagram:
            # Apply bonus as percentage increase, not fixed points
            bonus_amount = base_score * (diagram_bonus / 100)
            final_score = min(max_score, round(base_score + bonus_amount, 2))
        else:
            final_score = base_score
        
        return base_score, final_score


# Convenience functions
def determine_grade(score: float, max_score: float = 10.0) -> str:
    """Determine letter grade from score."""
    return GradeCalculator.from_score(score, max_score)


def determine_grade_from_percentage(percentage: float) -> str:
    """Determine letter grade from percentage."""
    return GradeCalculator.from_percentage(percentage)


def grammar_score(text: str) -> float:
    """Calculate grammar score."""
    return GrammarScorer.score(text)


def coverage_score(reference: str, student: str, threshold: int = 70) -> float:
    """Calculate coverage score."""
    return CoverageScorer.score(reference, student, threshold)


def generate_feedback(
    score: float,
    similarity: float,
    coverage: float,
    grammar: float,
    relevance: float,
    max_score: float = 10.0
) -> str:
    """Generate feedback."""
    return FeedbackGenerator.generate(score, similarity, coverage, grammar, relevance, max_score)
