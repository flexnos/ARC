"""
Quick test to verify backend is working correctly.
Run this to test the /evaluate endpoint directly.
"""

import requests
import json

print("=" * 60)
print("🧪 TESTING BACKEND /evaluate ENDPOINT")
print("=" * 60)

url = "http://localhost:8000/evaluate"

test_data = {
    "question": "What is artificial intelligence?",
    "reference_answer": "Artificial intelligence is the simulation of human intelligence processes by machines, especially computer systems.",
    "student_answer": "AI stands for Artificial Intelligence which means computers can think and act like humans by simulating human intelligence.",
    "model_name": None,
    "student_name": None
}

print("\n📤 Sending request to backend...")
print(f"URL: {url}")
print(f"Data: {json.dumps(test_data, indent=2)}\n")

try:
    response = requests.post(url, json=test_data)
    
    print(f"📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n✅ SUCCESS! Backend is working!\n")
        print("=" * 60)
        print("📋 RESPONSE:")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        
        print("\n" + "=" * 60)
        print("✅ FIELD VALIDATION:")
        print("=" * 60)
        
        checks = {
            "question": result.get('question'),
            "student_answer": result.get('student_answer'),
            "similarity": result.get('similarity'),
            "coverage": result.get('coverage'),
            "grammar": result.get('grammar'),
            "relevance": result.get('relevance'),
            "final_score": result.get('final_score'),
            "grade": result.get('grade'),
            "feedback": result.get('feedback'),
            "evaluation_id": result.get('evaluation_id'),
            "processing_time_ms": result.get('processing_time_ms')
        }
        
        all_good = True
        for field, value in checks.items():
            status = "✅" if value is not None else "❌"
            if value is None:
                all_good = False
            print(f"{status} {field}: {value if value else 'MISSING'}")
        
        print("\n" + "=" * 60)
        if all_good:
            print("🎉 ALL FIELDS PRESENT! Backend is working perfectly!")
        else:
            print("⚠️  SOME FIELDS MISSING! Check backend code.")
        print("=" * 60)
        
    elif response.status_code == 422:
        print(f"\n❌ VALIDATION ERROR (422)")
        print(f"Detail: {response.json().get('detail', 'Unknown error')}")
        print("\nThis means the payload format is wrong.")
        print("Check that question, reference_answer, and student_answer are not empty.")
        
    elif response.status_code == 500:
        print(f"\n❌ INTERNAL SERVER ERROR (500)")
        print(f"Detail: {response.text}")
        print("\nThis means backend crashed during processing.")
        print("Check backend terminal for error details.")
        
    else:
        print(f"\n❌ UNEXPECTED ERROR ({response.status_code})")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ CONNECTION ERROR")
    print("Backend is not running on http://localhost:8000")
    print("\nTo fix:")
    print("1. Open terminal")
    print("2. Run: cd d:\\D down\\bit")
    print("3. Run: python -m uvicorn main:app --host 127.0.0.1 --port 8000")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
