# 🐛 Text Evaluation Debugging Guide

## Let's Find Out What's Wrong

### Step 1: Check Browser Console (F12)

1. Open http://localhost:3000
2. Press **F12** to open DevTools
3. Click "Text" tab
4. Paste some text in the answer box
5. Click "Evaluate Answer"
6. Look at the **Console** tab

**What do you see?**

#### ❌ If you see red error:
```
Error: Backend error: ...
```
→ **Problem:** Backend is rejecting the request

#### ❌ If you see:
```
Failed to fetch
```
→ **Problem:** Backend isn't running on port 8000

#### ❌ If you see:
```
CORS policy blocked
```
→ **Problem:** CORS not enabled on backend

---

### Step 2: Check Backend Terminal

Look at the terminal where uvicorn is running. What does it show?

#### ✅ Success:
```
INFO: POST /evaluate HTTP/1.1" 200 OK
```

#### ❌ Validation Error (422):
```
INFO: POST /evaluate HTTP/1.1" 422 Unprocessable Entity
```
**Meaning:** Payload format is wrong

#### ❌ Server Error (500):
```
INFO: POST /evaluate HTTP/1.1" 500 Internal Server Error
```
**Meaning:** Backend crashed during evaluation

#### ❌ No Request:
```
(No new lines appear when you click evaluate)
```
**Meaning:** Frontend isn't sending request

---

### Step 3: Quick Test - Use Swagger UI

Instead of using the React UI, test your backend directly:

1. Open: http://localhost:8000/docs
2. Find `/evaluate` endpoint
3. Click "Try it out"
4. Fill in:
   ```json
   {
     "question": "Test question",
     "reference_answer": "This is a test answer",
     "student_answer": "This is a student answer"
   }
   ```
5. Click "Execute"

**What happens?**

#### ✅ Returns JSON with score:
```json
{
  "final_score": 8.5,
  "grade": "A",
  ...
}
```
→ **Backend works!** Problem is in frontend code.

#### ❌ Returns 422 error:
```json
{
  "detail": [...]
}
```
→ **Backend validation issue** - check field requirements

#### ❌ Returns 500 error:
```json
{
  "detail": "Internal server error"
}
```
→ **Backend crash** - check model loading

---

### Step 4: Common Issues & Fixes

#### Issue 1: Backend Not Running
**Check:**
```bash
# In backend terminal, should show:
INFO: Uvicorn running on http://127.0.0.1:8000
```

**Fix if not running:**
```bash
cd "d:\D down\bit"
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

---

#### Issue 2: CORS Not Enabled
**Add to `main.py`:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

#### Issue 3: Wrong Payload Format
**Frontend sends:**
```typescript
{
  "question": "...",
  "reference_answer": "...",  // Can't be empty!
  "student_answer": "..."
}
```

**Backend expects all fields min_length=1**

---

#### Issue 4: Model Loading Fails
**Check backend logs for:**
```
Loaded sentence transformer: MiniLM-L6
Loaded CNN model
Loaded tokenizer
```

If models fail to load, evaluation won't work.

---

### Step 5: Manual curl Test

Open a NEW terminal and run:

```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is AI?",
    "reference_answer": "AI stands for Artificial Intelligence",
    "student_answer": "Artificial Intelligence is simulated by computers"
  }'
```

**Expected response:**
```json
{
  "final_score": 7.5,
  "grade": "B",
  "percentage": 75,
  ...
}
```

**If this works** → Backend is fine, problem is frontend  
**If this fails** → Backend has issues

---

### Step 6: Check These Files Exist

Make sure these files are in `d:\D down\bit\`:

- ✅ `main.py` (backend API)
- ✅ `models.py` (model loading)
- ✅ `scoring.py` (scoring logic)
- ✅ `config.py` (configuration)
- ✅ `security.py` (validation)
- ✅ `database.py` (storage)
- ✅ `pdf_processor.py` (PDF handling)
- ✅ `auto_ref_generator.py` (reference generation)

---

### Step 7: Verify Dependencies Installed

Run in backend directory:
```bash
pip list | findstr fastapi
pip list | findstr uvicorn
pip list | findstr sentence-transformers
```

Should show:
```
fastapi                0.109.0
uvicorn                0.27.0
sentence-transformers  2.3.0
```

If missing:
```bash
pip install fastapi uvicorn sentence-transformers
```

---

## 🎯 Most Likely Issues

Based on your setup, here are the most common problems:

### 1. **Backend Port Already in Use**
You had this earlier! Check:
```bash
npx kill-port 8000
```

Then restart backend.

---

### 2. **Models Not Loading**
First-time model loading takes time. Backend logs should show:
```
Loaded sentence transformer: MiniLM-L6
Loaded sentence transformer: mpnet
Loaded CNN model
Loaded tokenizer
```

Wait for these messages before testing!

---

### 3. **Frontend Sending Wrong Data**
Check browser Network tab (F12):
1. Click "Evaluate"
2. Find `/evaluate` request
3. Right-click → "Copy as cURL"
4. Paste somewhere to inspect payload

Verify:
- `question` is not empty
- `reference_answer` is not empty (even in auto mode)
- `student_answer` has your text

---

### 4. **Auto Reference Mode Confusion**
In auto mode:
- Frontend sends student answer as reference placeholder
- Backend should generate its own reference
- Backend evaluates against generated reference

If backend doesn't have auto-reference logic implemented, it will just compare student answer to itself (which gives perfect score!).

---

## 💡 Quick Solution

If nothing else works, try this minimal test:

### 1. Start Fresh
Close both terminals

### 2. Start Backend Only
```bash
cd "d:\D down\bit"
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Wait for: `INFO: Application startup complete.`

### 3. Test with Swagger
Open: http://localhost:8000/docs

Click `/evaluate` → Try it out → Execute

**If this works** → Backend is good, frontend has issues  
**If this fails** → Backend needs fixing first

### 4. Then Start Frontend
NEW terminal:
```bash
cd "d:\D down\bit\ui-react"
npm run dev
```

### 5. Test Again
Open: http://localhost:3000 → Text tab → Evaluate

---

## 📞 Tell Me What You See

After trying these steps, tell me:

1. **Browser console errors?** (Copy exact message)
2. **Backend terminal shows?** (When you click evaluate)
3. **Swagger UI test result?** (Works or fails?)
4. **curl test result?** (JSON response or error?)

With this info, I can give you the exact fix! 🎯
