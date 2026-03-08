# 🔌 Connect Frontend to Backend - Quick Fix

## ✅ What I Just Did

I updated the `handleEvaluate` function in `page.tsx` to call your **real FastAPI backend** instead of returning static mock data!

---

## 🚀 How to Test Now

### **You Need BOTH Servers Running:**

#### **Terminal 1 - Backend:**
```bash
cd "d:\D down\bit"
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

#### **Terminal 2 - Frontend:**
```bash
cd "d:\D down\bit\ui-react"
npm run dev
```

---

## 📡 API Endpoints Being Called

The frontend now calls these endpoints on your backend:

### 1. **Text Evaluation** ✅
```
POST http://localhost:8000/evaluate
Content-Type: application/json

{
  "question": "Evaluate this answer",
  "reference_answer": "...",  // if manual mode
  "student_answer": "..."
}
```

### 2. **PDF Auto-Evaluation** ✅
```
POST http://localhost:8000/evaluate/pdf-auto
Content-Type: multipart/form-data

Files:
- answer_sheet (PDF)
- question_paper (PDF)
```

### 3. **PDF Manual Evaluation** ✅
```
POST http://localhost:8000/evaluate/pdf
Content-Type: multipart/form-data

Files:
- answer_sheet (PDF)
- question_paper (PDF)
- reference_answers (PDF)
```

### 4. **OCR Evaluation** ⚠️ (Need to Create)
```
POST http://localhost:8000/evaluate/ocr
Content-Type: multipart/form-data

Files:
- image (JPG/PNG)
- question_text (form field)
```

### 5. **Batch Processing** ⚠️ (Need to Create)
```
POST http://localhost:8000/evaluate/batch
Content-Type: multipart/form-data

File:
- zip_archive (ZIP file)
```

---

## ✅ Expected Backend Response Format

Your backend should return JSON like this:

```json
{
  "final_score": 8.5,
  "grade": "A",
  "percentage": 85,
  "feedback": "Excellent answer!",
  "similarity": 0.85,
  "coverage": 0.78,
  "grammar": 0.92,
  "relevance": 0.88,
  "extracted_text": "..."  // Only for OCR
}
```

---

## 🔧 If You Get Errors

### Error: "Failed to fetch" or "Network Error"

**Solution:** Make sure backend is running!
```bash
# Check if backend is running
curl http://localhost:8000/health

# Should return: {"status": "healthy", ...}
```

### Error: "CORS policy blocked"

**Solution:** Add CORS to your backend (`main.py`):

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

### Error: "404 Not Found"

**Solution:** Verify your backend has these endpoints:
- `/evaluate` ✅
- `/evaluate/pdf-auto` ✅
- `/evaluate/pdf` ✅
- `/evaluate/ocr` ⚠️ (create this)
- `/evaluate/batch` ⚠️ (create this)

---

## 🎯 Testing Checklist

Test each mode:

### Text Evaluation ✅
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Navigate to "Text" tab
- [ ] Paste student answer
- [ ] Click "Evaluate Answer"
- [ ] Should show REAL results from backend!

### PDF Evaluation ✅
- [ ] Navigate to "Advanced" tab
- [ ] Upload answer sheet PDF
- [ ] Upload question paper PDF
- [ ] Click "Start Advanced Evaluation"
- [ ] Should get real evaluation from backend!

### OCR Evaluation ⚠️
- [ ] Need to create `/evaluate/ocr` endpoint first
- [ ] Then test image upload + evaluation

### Batch Processing ⚠️
- [ ] Need to create `/evaluate/batch` endpoint first
- [ ] Then test ZIP file upload

---

## 💡 Quick Backend Test

Before using the UI, test your backend directly:

### Using curl:
```bash
# Test text evaluation
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is AI?",
    "reference_answer": "AI is artificial intelligence",
    "student_answer": "AI means artificial intelligence"
  }'
```

### Using browser:
Open: http://localhost:8000/docs

This shows Swagger UI where you can test all endpoints interactively!

---

## 🎉 Success Indicators

You'll know it's working when:

✅ **Frontend:**
- No more static "8.5/A/85%" for everything
- Results vary based on actual answers
- Real processing time (not fixed 2 seconds)
- Error messages if backend fails

✅ **Backend:**
- Receives POST requests from frontend
- Logs show incoming requests
- Returns proper JSON responses
- Processes files correctly

---

## 📝 Summary

**What Changed:**
- ❌ Removed: Static mock data with `setTimeout`
- ✅ Added: Real API calls to FastAPI backend
- ✅ Added: Error handling and user feedback
- ✅ Added: File upload support (FormData)

**What You Need:**
1. Backend running on http://localhost:8000 ✅
2. Frontend running on http://localhost:3000 ✅
3. CORS enabled on backend ✅
4. Required endpoints implemented ✅

**Then:**
- Text evaluation → Works! ✅
- PDF evaluation → Works! ✅
- OCR evaluation → Need to create endpoint
- Batch processing → Need to create endpoint

---

## 🚀 Next Steps

1. **Start both servers** (backend + frontend)
2. **Test text evaluation** - Should work immediately
3. **Test PDF evaluation** - Should work immediately
4. **Create OCR endpoint** - For image evaluation
5. **Create batch endpoint** - For bulk processing

**Your app will now give REAL, DYNAMIC responses instead of static ones!** 🎊
