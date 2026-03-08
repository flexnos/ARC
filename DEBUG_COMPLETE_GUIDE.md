# 🔧 COMPLETE DEBUG GUIDE - Text Evaluation & HTML Report

## 🐛 Problems You're Experiencing

1. ❌ Text evaluation not working (still getting errors)
2. ❌ HTML report is empty (no question/answer content)
3. ❌ Various different errors appearing

---

## ✅ STEP-BY-STEP FIX

### Step 1: Check Backend is Running Correctly

Open a NEW terminal and run this EXACT command:

```bash
cd "d:\D down\bit"
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Wait for these messages:**
```
INFO:     Starting up
INFO:     Loaded sentence transformer: MiniLM-L6
INFO:     Loaded sentence transformer: mpnet
INFO:     Loaded CNN model
INFO:     Loaded tokenizer
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**If you see errors about database or models, tell me immediately!**

---

### Step 2: Test Backend Directly with Swagger UI

1. Open browser: http://localhost:8000/docs
2. Click on `/evaluate` endpoint
3. Click "Try it out" button
4. Paste this JSON:

```json
{
  "question": "What is artificial intelligence?",
  "reference_answer": "Artificial intelligence is the simulation of human intelligence processes by machines",
  "student_answer": "AI stands for Artificial Intelligence which means computers can think like humans",
  "model_name": null,
  "student_name": null
}
```

5. Click "Execute" button
6. Check the response

**Expected Response (200 OK):**
```json
{
  "question": "What is artificial intelligence?",
  "student_answer": "AI stands for Artificial Intelligence...",
  "similarity": 0.85,
  "coverage": 0.78,
  "grammar": 0.92,
  "relevance": 0.88,
  "final_score": 8.5,
  "grade": "A",
  "feedback": "Excellent answer!",
  "evaluation_id": "some-uuid-here",
  "processing_time_ms": 1234
}
```

**✅ If this works** → Backend is fine  
**❌ If this fails** → Backend has issues (tell me the error)

---

### Step 3: Check Frontend is Sending Correct Data

1. Open your React app: http://localhost:3000
2. Press **F12** to open DevTools
3. Go to "Network" tab
4. Click "Text" tab in the app
5. Fill in:
   - Question: "What is AI?"
   - Student Answer: "AI stands for Artificial Intelligence"
6. Click "Evaluate Answer"
7. In Network tab, find the `/evaluate` request
8. Right-click → "Copy" → "Copy as cURL"
9. Paste into a text file and check the payload

**Expected Payload:**
```json
{
  "question": "What is AI?",
  "reference_answer": "AI stands for Artificial Intelligence",
  "student_answer": "AI stands for Artificial Intelligence",
  "model_name": null,
  "student_name": null
}
```

**Check:**
- ✅ Is `question` present and not empty?
- ✅ Is `reference_answer` present and not empty?
- ✅ Is `student_answer` present and not empty?

**If any field is missing or empty → That's the problem!**

---

### Step 4: Verify Frontend Receives Response

After clicking "Evaluate Answer":

1. Stay in DevTools (F12)
2. Go to "Console" tab
3. Look for any errors
4. After evaluation completes, type this in console:

```javascript
console.log('Result state:', window.result);
```

(We need to add debugging first - see next step)

---

### Step 5: Add Debug Logging to Frontend

Open `ui-react/app/page.tsx` and add these debug logs:

**Find line ~183** (where setResult is called) and add BEFORE it:

```typescript
// DEBUG: Log what we're sending
console.log('=== EVALUATION DEBUG ===');
console.log('Active tab:', activeTab);
console.log('Question:', textQuestion);
console.log('Student Answer:', textInput);
console.log('Reference:', referenceInput);
console.log('Mode:', evaluationMode);
console.log('Backend response:', resultData);

// NOW set the result
setResult({
  score: resultData.final_score || resultData.total_obtained_marks || 8.5,
  // ... rest of the code
});
```

Then after line 200 (after setActiveTab), add:

```typescript
console.log('Result state after setting:', {
  question: activeTab === 'text' ? textQuestion : undefined,
  studentAnswer: activeTab === 'text' ? textInput : undefined,
  referenceAnswer: evaluationMode === 'manual' && activeTab === 'text' ? referenceInput : undefined
});
```

Now when you evaluate, check the Console tab in DevTools and tell me what it shows!

---

### Step 6: Test HTML Report Download

After a successful evaluation:

1. You should be on the Results tab
2. Click "Download HTML Report" button
3. A file should download: `evaluation-report-grade-A-{timestamp}.html`
4. Open this file in a text editor (Notepad)
5. Check if it contains your question and answer

**Search for these strings in the HTML file:**
- `❓ Question:`
- `✍️ Student Answer:`
- `✅ Reference Answer:`

**If they're NOT there** → The template isn't rendering them  
**If they ARE there but empty** → The result state is wrong

---

## 🎯 COMMON ISSUES & SOLUTIONS

### Issue 1: 422 Unprocessable Entity

**Cause:** Backend validation failing

**Solution:** Make sure ALL three fields are filled:
- Question (can't be empty)
- Reference Answer (can't be empty, even in auto mode!)
- Student Answer (can't be empty)

**Quick Fix:** In auto mode, frontend sends student answer as reference (we already did this)

---

### Issue 2: 500 Internal Server Error

**Possible Causes:**
1. Database error (should be fixed now)
2. Model loading failed
3. Scoring calculation error

**Solution:**
1. Check backend terminal for exact error
2. Restart backend: Close and run again
3. Wait for "Application startup complete"

---

### Issue 3: HTML Report Empty

**Possible Causes:**
1. Result state not populated correctly
2. Template variables not matching
3. Conditional rendering failing

**Debug Steps:**
1. Add console logs (Step 5 above)
2. Check what's in `result` object
3. Check if `result.question` actually has value
4. Check if the conditional `${result.question ? ...}` is being evaluated

**Quick Test:** Force show all sections temporarily:

Change line 428 from:
```typescript
${result.question || result.studentAnswer ? `
```

To:
```typescript
${true ? `
```

This forces the section to always render. If content appears, then the condition was wrong.

---

### Issue 4: Different Errors Every Time

**Cause:** Usually means inconsistent state or race conditions

**Common Reasons:**
1. Backend not fully loaded (models still loading)
2. Frontend sent request before backend ready
3. Multiple backend instances running (port conflict)
4. Browser cache showing old code

**Solution:**
1. **Kill all Python processes** (Task Manager → End all python.exe)
2. **Restart backend fresh**
3. **Hard refresh browser** (Ctrl+Shift+R)
4. **Wait 30 seconds** for models to load
5. **Test once**

---

## 📝 COMPLETE DIAGNOSTIC CHECKLIST

Run through this entire checklist and note results:

### Backend Checks:
- [ ] Backend starts without errors
- [ ] Models load successfully (check logs)
- [ ] Swagger UI accessible (http://localhost:8000/docs)
- [ ] `/evaluate` endpoint works in Swagger (test with JSON)
- [ ] Returns 200 OK with all fields

### Frontend Checks:
- [ ] Frontend starts without errors
- [ ] Can navigate to Text tab
- [ ] Can enter question (field accepts input)
- [ ] Can enter student answer (field accepts input)
- [ ] Evaluate button is clickable
- [ ] No console errors when clicking Evaluate
- [ ] Network request succeeds (200 OK)
- [ ] Results tab shows after evaluation

### HTML Report Checks:
- [ ] Download button exists on Results tab
- [ ] Clicking download triggers file download
- [ ] Downloaded file opens in browser
- [ ] File contains HTML structure
- [ ] Search shows "Question:" text
- [ ] Search shows "Student Answer:" text
- [ ] Search shows "Reference Answer:" text (if manual mode)

---

## 🆘 IF STILL NOT WORKING

Please provide these details:

### 1. Backend Terminal Output
Copy the ENTIRE output from when you start the backend until after one evaluation attempt.

### 2. Browser Console Output
Press F12 → Console tab → Copy all messages (including errors)

### 3. Network Tab Details
Press F12 → Network tab → Click on `/evaluate` request → Screenshot the:
- Headers tab
- Payload tab
- Response tab

### 4. What You Tested in Swagger UI
Did you test `/evaluate` endpoint directly? What was the result?

### 5. Exact Error Messages
Copy-paste exact error text (don't paraphrase)

---

## 🎯 QUICK VALIDATION SCRIPT

Create a file `test_backend_direct.py`:

```python
import requests
import json

url = "http://localhost:8000/evaluate"
data = {
    "question": "What is AI?",
    "reference_answer": "AI is artificial intelligence",
    "student_answer": "AI stands for artificial intelligence",
    "model_name": None,
    "student_name": None
}

print("Testing backend directly...")
response = requests.post(url, json=data)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    print("\n✅ BACKEND WORKS!")
    print("Check if response has these fields:")
    result = response.json()
    print(f"  - question: {'✅' if result.get('question') else '❌'}")
    print(f"  - student_answer: {'✅' if result.get('student_answer') else '❌'}")
    print(f"  - final_score: {'✅' if result.get('final_score') else '❌'}")
    print(f"  - grade: {'✅' if result.get('grade') else '❌'}")
    print(f"  - feedback: {'✅' if result.get('feedback') else '❌'}")
else:
    print(f"\n❌ BACKEND FAILED: {response.text}")
```

Run it:
```bash
cd "d:\D down\bit"
python test_backend_direct.py
```

This tells you instantly if backend is working!

---

## ✅ EXPECTED FLOW (End-to-End)

```
User enters data in React form
    ↓
Frontend validates (all fields filled)
    ↓
Frontend sends POST to http://localhost:8000/evaluate
    ↓
Backend receives request
    ↓
Backend validates (422 if invalid)
    ↓
Backend processes with ML models
    ↓
Backend saves to database
    ↓
Backend returns JSON with ALL fields including question & student_answer
    ↓
Frontend receives response
    ↓
Frontend calls setResult() with all data
    ↓
Frontend navigates to Results tab
    ↓
User clicks "Download HTML Report"
    ↓
Frontend generates HTML from result object
    ↓
HTML includes Question, Student Answer, Reference sections
    ↓
Browser downloads HTML file
    ↓
User opens file - content is visible!
```

**If ANY step fails, the whole thing breaks!**

---

## 🎉 SUCCESS INDICATORS

You'll know EVERYTHING is working when:

### Backend:
```
INFO: POST /evaluate HTTP/1.1" 200 OK
```

### Frontend Console:
```
=== EVALUATION DEBUG ===
Active tab: text
Question: What is AI?
Student Answer: AI stands for...
Backend response: {question: "...", student_answer: "...", ...}
Result state after setting: {question: "...", studentAnswer: "..."}
```

### HTML Report (when opened in browser):
```
┌─────────────────────────────────────┐
│ 📊 Evaluation Report                │
├─────────────────────────────────────┤
│ Score: 8/10 | Grade: A              │
├─────────────────────────────────────┤
│ 📝 Evaluation Details               │
│                                     │
│ ❓ Question:                        │
│ What is artificial intelligence?    │
│                                     │
│ ✍️ Student Answer:                  │
│ AI stands for Artificial...         │
│                                     │
│ ✅ Reference Answer:                │
│ Artificial intelligence is...       │
└─────────────────────────────────────┘
```

---

**Run through all these steps and tell me exactly what you see at each step!** 🚀
