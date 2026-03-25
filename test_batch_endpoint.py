"""
Test script for batch evaluation endpoint.
Tests the /evaluate/batch API with the batch_test.zip file.
"""

import requests
import json

# API endpoint
URL = "http://127.0.0.1:8000/evaluate/batch"

# Test with auto-reference generation
print("🧪 Testing Batch Evaluation Endpoint...")
print("=" * 60)

try:
    # Read the ZIP file
    with open('batch_test.zip', 'rb') as f:
        files = {'batch_file': ('batch_test.zip', f, 'application/zip')}
        
        # Form data - enable auto_ref mode
        data = {
            'auto_ref': 'true'
        }
        
        print("\n📤 Sending request to:", URL)
        print("📦 File: batch_test.zip")
        print("⚙️  Mode: Auto-reference generation")
        
        response = requests.post(URL, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ SUCCESS!")
            print("=" * 60)
            print(f"📊 Evaluation ID: {result['evaluation_id']}")
            print(f"📝 Question: {result['question'][:100]}...")
            print(f"📖 Reference Answer: {result['reference_answer'][:100]}...")
            print(f"\n👥 Total Students: {result['total_students']}")
            print(f"📈 Average Score: {result['average_score']}")
            print(f"🏆 Highest Score: {result['highest_score']}")
            print(f"📉 Lowest Score: {result['lowest_score']}")
            print(f"⏱️  Processing Time: {result['processing_time_ms']}ms")
            
            print("\n" + "=" * 60)
            print("📋 Individual Results:")
            print("=" * 60)
            
            for i, res in enumerate(result['results'], 1):
                print(f"\n{i}. {res['student_name']}")
                print(f"   Score: {res['final_score']}/10 | Grade: {res['grade']}")
                print(f"   Similarity: {res['similarity']} | Coverage: {res['coverage']}")
                print(f"   Grammar: {res['grammar']} | Relevance: {res['relevance']}")
                print(f"   Feedback: {res['feedback']}")
            
            print("\n" + "=" * 60)
            print("💾 Full JSON Response:")
            print("=" * 60)
            print(json.dumps(result, indent=2))
            
        else:
            print(f"\n❌ FAILED with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
except FileNotFoundError:
    print("\n❌ Error: batch_test.zip not found!")
    print("   Make sure you're in the correct directory.")
except requests.exceptions.ConnectionError:
    print("\n❌ Error: Cannot connect to server!")
    print("   Make sure the backend is running: python app.py")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("Test complete!")
