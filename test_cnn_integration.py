"""Test script for CNN integration"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test data
test_data = {
    "question": "Explain the process of photosynthesis in plants.",
    "reference_answer": "Photosynthesis is the process by which plants convert light energy into chemical energy. Plants use chlorophyll to absorb sunlight, and combine carbon dioxide from the air with water to produce glucose and oxygen. This process occurs in the chloroplasts of plant cells.",
    "student_answer": "Photosynthesis is how plants make food using sunlight. They take in CO2 and water, and use light energy to create glucose and release oxygen. It happens in chloroplasts where chlorophyll captures light."
}

print("Testing CNN Integration")
print("=" * 50)

# Test 1: Evaluate without CNN
print("\n1. Testing WITHOUT CNN...")
try:
    response1 = requests.post(f"{BASE_URL}/evaluate", json=test_data)
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"✓ Score without CNN: {result1['final_score']}/10")
        print(f"  Grade: {result1['grade']}")
        print(f"  Similarity: {result1['similarity']}")
    else:
        print(f"✗ Error: {response1.status_code}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: Evaluate with CNN
print("\n2. Testing WITH CNN...")
try:
    response2 = requests.post(f"{BASE_URL}/evaluate?use_cnn=true", json=test_data)
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"✓ Score with CNN: {result2['final_score']}/10")
        print(f"  Grade: {result2['grade']}")
        print(f"  Similarity: {result2['similarity']}")
        if 'cnn_score' in result2:
            print(f"  CNN Score: {result2['cnn_score']}")
    else:
        print(f"✗ Error: {response2.status_code}")
        print(f"Response: {response2.text}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 3: Health check
print("\n3. Checking model health...")
try:
    response3 = requests.get(f"{BASE_URL}/health")
    if response3.status_code == 200:
        health = response3.json()
        print(f"✓ Health Status: {health['status']}")
        print(f"  CNN Loaded: {health['models']['cnn_model_loaded']}")
        print(f"  Tokenizer Loaded: {health['models']['tokenizer_loaded']}")
        print(f"  Sentence Transformers: {health['models']['sentence_transformers_loaded']}")
    else:
        print(f"✗ Error: {response3.status_code}")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n" + "=" * 50)
print("Test complete!")
