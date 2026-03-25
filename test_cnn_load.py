"""
Test script to diagnose CNN model compatibility and try alternative loading methods
"""
import pickle
from tensorflow.keras.models import load_model
import tensorflow as tf

print(f"TensorFlow version: {tf.__version__}")
print("\nAttempting to load CNN model...")

try:
    # Try standard loading
    model = load_model('cnn_answer_evaluator.h5')
    print("✓ Standard load successful")
    print(f"  Input shape: {model.input_shape}")
    print(f"  Output shape: {model.output_shape}")
except Exception as e:
    print(f"✗ Standard load failed: {e}")
    
    try:
        # Try without compiling
        print("\nTrying to load without compilation...")
        model = load_model('cnn_answer_evaluator.h5', compile=False)
        print("✓ Load without compile successful")
        print(f"  Input shape: {model.input_shape}")
        print(f"  Output shape: {model.output_shape}")
    except Exception as e2:
        print(f"✗ Load without compile also failed: {e2}")
        
        # Try loading weights only
        try:
            print("\nModel architecture might be incompatible.")
            print("The model file exists but uses an older Keras format.")
            print("\nRecommendation: Retrain the CNN model with current TensorFlow version")
        except:
            pass

# Check tokenizer
print("\nLoading tokenizer...")
try:
    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    print("✓ Tokenizer loaded successfully")
    if hasattr(tokenizer, 'word_index'):
        print(f"  Vocabulary size: {len(tokenizer.word_index)}")
except Exception as e:
    print(f"✗ Tokenizer failed: {e}")
