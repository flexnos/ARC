"""Test script to understand CNN model structure"""
import pickle
from tensorflow.keras.models import load_model
import numpy as np

print("Loading CNN model...")
model = load_model('cnn_answer_evaluator.h5')
print(f"✓ Model loaded successfully")
print(f"\nInput shape: {model.input_shape}")
print(f"Output shape: {model.output_shape}")

print("\nLoading tokenizer...")
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)
print(f"✓ Tokenizer loaded successfully")
print(f"Tokenizer type: {type(tokenizer)}")
print(f"Tokenizer attributes: {[attr for attr in dir(tokenizer) if not attr.startswith('_')][:10]}")

# Try to get word index if available
if hasattr(tokenizer, 'word_index'):
    print(f"\nVocabulary size: {len(tokenizer.word_index)}")
    sample_words = list(tokenizer.word_index.keys())[:10]
    print(f"Sample words: {sample_words}")

# Test tokenization
test_text = "This is a sample answer for testing"
print(f"\nTesting tokenization with: '{test_text}'")
sequences = tokenizer.texts_to_sequences([test_text])
print(f"Tokenized sequence: {sequences}")

# Check max length
if hasattr(tokenizer, 'word_index'):
    max_len = max([len(seq) for seq in sequences])
    print(f"Sequence length: {max_len}")

print("\n✅ Model analysis complete!")
