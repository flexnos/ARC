"""
Model management module for Answer Evaluation System.
Handles loading and caching of ML models.
"""

import os
import pickle
import logging
from typing import Dict, Optional, Any
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer, util

from config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class ModelManager:
    """Manages ML models for answer evaluation."""
    
    def __init__(self):
        self.sentence_transformers: Dict[str, SentenceTransformer] = {}
        self.cnn_model: Optional[Any] = None
        self.tokenizer: Optional[Any] = None
        self.default_model: str = settings.DEFAULT_MODEL
        self._load_models()
    
    def _load_models(self):
        """Load all configured models."""
        # Load sentence transformers
        for model_name in settings.sentence_transformer_models_list:
            try:
                # Create a friendly name from the model path
                friendly_name = model_name.split('/')[-1].replace('all-', '').replace('-v2', '').replace('-base', '')
                self.sentence_transformers[friendly_name] = SentenceTransformer(model_name)
                logger.info(f"Loaded sentence transformer: {friendly_name}")
            except Exception as e:
                logger.error(f"Failed to load sentence transformer {model_name}: {e}")
        
        # Load CNN model if available
        try:
            if os.path.exists(settings.CNN_MODEL_PATH):
                from tensorflow.keras.models import load_model
                self.cnn_model = load_model(settings.CNN_MODEL_PATH)
                logger.info("Loaded CNN model")
            else:
                logger.warning(f"CNN model not found at {settings.CNN_MODEL_PATH}")
        except Exception as e:
            logger.warning(f"Failed to load CNN model: {e}")
            self.cnn_model = None
        
        # Load tokenizer if available
        try:
            if os.path.exists(settings.TOKENIZER_PATH):
                with open(settings.TOKENIZER_PATH, "rb") as f:
                    self.tokenizer = pickle.load(f)
                logger.info("Loaded tokenizer")
            else:
                logger.warning(f"Tokenizer not found at {settings.TOKENIZER_PATH}")
        except Exception as e:
            logger.warning(f"Failed to load tokenizer: {e}")
            self.tokenizer = None
    
    def get_sentence_transformer(self, model_name: Optional[str] = None) -> Optional[SentenceTransformer]:
        """Get a sentence transformer model by name."""
        model_name = model_name or self.default_model
        
        # Try exact match first
        if model_name in self.sentence_transformers:
            return self.sentence_transformers[model_name]
        
        # Try case-insensitive match
        for name, model in self.sentence_transformers.items():
            if name.lower() == model_name.lower():
                return model
        
        # Return first available if default not found
        if self.sentence_transformers:
            return next(iter(self.sentence_transformers.values()))
        
        return None
    
    def compute_similarity(
        self,
        reference: str,
        student: str,
        model_name: Optional[str] = None
    ) -> float:
        """Compute semantic similarity between two texts."""
        model = self.get_sentence_transformer(model_name)
        
        if not model:
            logger.error("No sentence transformer model available")
            return 0.0
        
        try:
            ref_emb = model.encode(reference, convert_to_tensor=True)
            student_emb = model.encode(student, convert_to_tensor=True)
            similarity = util.cos_sim(ref_emb, student_emb).item()
            # Normalize to 0-1 range
            return round((similarity + 1) / 2, 3)
        except Exception as e:
            logger.error(f"Similarity calculation error: {e}")
            return 0.0
    
    def compute_relevance(
        self,
        question: str,
        answer: str,
        model_name: Optional[str] = None
    ) -> float:
        """Compute relevance of answer to question."""
        model = self.get_sentence_transformer(model_name)
        
        if not model:
            logger.error("No sentence transformer model available")
            return 0.5
        
        try:
            q_emb = model.encode(question, convert_to_tensor=True)
            a_emb = model.encode(answer, convert_to_tensor=True)
            relevance = util.cos_sim(q_emb, a_emb).item()
            # Normalize to 0-1 range
            return round((relevance + 1) / 2, 3)
        except Exception as e:
            logger.error(f"Relevance calculation error: {e}")
            return 0.5
    
    def get_available_models(self) -> Dict[str, bool]:
        """Get list of available models."""
        return {
            "sentence_transformers": list(self.sentence_transformers.keys()),
            "default_model": self.default_model,
            "cnn_available": self.cnn_model is not None,
            "tokenizer_available": self.tokenizer is not None
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check model health status."""
        return {
            "sentence_transformers_loaded": len(self.sentence_transformers),
            "sentence_transformer_models": list(self.sentence_transformers.keys()),
            "cnn_model_loaded": self.cnn_model is not None,
            "tokenizer_loaded": self.tokenizer is not None,
            "status": "healthy" if self.sentence_transformers else "unhealthy"
        }


# Global model manager instance
_model_manager: Optional[ModelManager] = None


def get_model_manager() -> ModelManager:
    """Get or create the global model manager."""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager
