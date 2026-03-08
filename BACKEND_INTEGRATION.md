# 🔌 Backend Integration Guide

## Quick Start - Connect React UI to FastAPI Backend

### Step 1: Install Axios (Optional but Recommended)

```bash
cd ui-react
npm install axios
```

---

### Step 2: Update page.tsx with Real API Calls

Find the `handleEvaluate` function in `ui-react/app/page.tsx` and replace it with this:

```typescript
const handleEvaluate = async () => {
  setIsProcessing(true);
  
  try {
    let response;
    const API_BASE = 'http://localhost:8000';
    
    // TEXT EVALUATION
    if (activeTab === 'text') {
      const payload = {
        question: 'Evaluate this answer', // You can add a question input field
        reference_answer: referenceInput,
        student_answer: textInput
      };
      
      response = await fetch(`${API_BASE}/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    }
    
    // ADVANCED PDF EVALUATION
    else if (activeTab === 'advanced') {
      const formData = new FormData();
      
      if (selectedFiles.answerSheet) {
        formData.append('answer_sheet', selectedFiles.answerSheet);
      }
      if (selectedFiles.questionPaper) {
        formData.append('question_paper', selectedFiles.questionPaper);
      }
      
      if (evaluationMode === 'manual') {
        if (selectedFiles.reference) {
          formData.append('reference_answers', selectedFiles.reference);
        }
        response = await fetch(`${API_BASE}/evaluate/pdf`, {
          method: 'POST',
          body: formData
        });
      } else {
        // Auto reference mode
        response = await fetch(`${API_BASE}/evaluate/pdf-auto`, {
          method: 'POST',
          body: formData
        });
      }
    }
    
    // OCR EVALUATION
    else if (activeTab === 'ocr') {
      const formData = new FormData();
      
      if (selectedFiles.ocrImage) {
        formData.append('image', selectedFiles.ocrImage);
      }
      
      // You'll need to create this endpoint on backend
      response = await fetch(`${API_BASE}/evaluate/ocr`, {
        method: 'POST',
        body: formData
      });
    }
    
    // BATCH PROCESSING
    else if (activeTab === 'batch') {
      const formData = new FormData();
      
      if (selectedFiles.batchFile) {
        formData.append('zip_archive', selectedFiles.batchFile);
      }
      
      // You'll need to create this endpoint on backend
      response = await fetch(`${API_BASE}/evaluate/batch`, {
        method: 'POST',
        body: formData
      });
    }
    
    if (response && response.ok) {
      const result = await response.json();
      setResult(result);
      setActiveTab('results');
    } else {
      throw new Error('Evaluation failed');
    }
    
  } catch (error) {
    console.error('Evaluation error:', error);
    alert('Evaluation failed: ' + (error as Error).message);
  } finally {
    setIsProcessing(false);
  }
};
```

---

### Step 3: Ensure CORS is Enabled on Backend

In your `main.py`, make sure CORS is configured:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Step 4: Test Each Mode

#### Test Text Evaluation:
1. Click "Text" tab
2. Paste a sample answer
3. Click "Evaluate Answer"
4. Should see results in Results tab

#### Test Advanced PDF:
1. Click "Advanced" tab
2. Drag answer sheet PDF
3. Drag question paper PDF
4. Click "Start Advanced Evaluation"
5. Should process and show results

#### Test OCR:
1. Click "OCR" tab
2. Upload image of handwritten answer
3. Click "Extract & Evaluate"
4. Should extract text and evaluate

#### Test Batch:
1. Click "Batch" tab
2. Upload ZIP file with multiple PDFs
3. Click "Start Batch Evaluation"
4. Should process all files

---

## 📝 Backend Endpoints Reference

Your backend should have these endpoints:

### 1. Text Evaluation
```
POST /evaluate
Content-Type: application/json

{
  "question": "string",
  "reference_answer": "string",
  "student_answer": "string"
}

Response:
{
  "final_score": 8.5,
  "grade": "A",
  "feedback": "Excellent!",
  "similarity": 0.85,
  "coverage": 0.78,
  "grammar": 0.92,
  "relevance": 0.88
}
```

### 2. PDF Auto-Evaluation
```
POST /evaluate/pdf-auto
Content-Type: multipart/form-data

Files:
- answer_sheet (PDF)
- question_paper (PDF)

Response:
{
  "total_obtained_marks": 42.5,
  "total_max_marks": 50,
  "percentage": 85,
  "grade": "A",
  "questions_results": [...]
}
```

### 3. PDF Manual Evaluation
```
POST /evaluate/pdf
Content-Type: multipart/form-data

Files:
- answer_sheet (PDF)
- question_paper (PDF)
- reference_answers (PDF)

Response: Same as above
```

### 4. OCR Evaluation (Create This)
```
POST /evaluate/ocr
Content-Type: multipart/form-data

Files:
- image (JPG/PNG)
- question_text (optional form field)

Response:
{
  "extracted_text": "Student's handwritten text...",
  "evaluation": {
    "score": 7.5,
    "grade": "B+",
    ...
  }
}
```

### 5. Batch Processing (Create This)
```
POST /evaluate/batch
Content-Type: multipart/form-data

Files:
- zip_archive (ZIP containing PDFs)

Response:
{
  "total_students": 10,
  "results": [
    {"student": "student1.pdf", "score": 8.5, ...},
    {"student": "student2.pdf", "score": 7.2, ...},
    ...
  ]
}
```

---

## 🔧 If You Get CORS Errors

Add this to your backend's main.py:

```python
from fastapi.middleware.cors import CORSMiddleware

# Allow all origins for development (use specific origin in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Common Issues & Solutions

### Issue: "Network Error"
**Solution:** Check that backend is running on http://localhost:8000

### Issue: "CORS policy blocked"
**Solution:** Add CORS middleware to backend (see above)

### Issue: "404 Not Found"
**Solution:** Verify endpoint URLs match your backend routes

### Issue: Files not uploading
**Solution:** Make sure to use FormData and set Content-Type to multipart/form-data

### Issue: TypeScript errors
**Solution:** These are just type warnings - the code will still work at runtime

---

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] CORS enabled on backend
- [ ] All endpoints responding correctly
- [ ] Text evaluation working
- [ ] PDF upload and evaluation working
- [ ] Image upload working
- [ ] File drag-and-drop functional
- [ ] Results displaying correctly

---

## 🎯 Next Steps After Integration

1. **Add Loading States:** Show progress bars during file upload
2. **Error Handling:** Display user-friendly error messages
3. **Success Notifications:** Toast notifications for successful evaluations
4. **History Feature:** Save past evaluations
5. **Export Results:** Download results as PDF/CSV
6. **File Size Limits:** Validate file sizes before upload
7. **Progress Tracking:** Show upload/download progress

---

**That's it!** Your professional AI evaluation system is now fully connected and ready to use! 🚀

Test it by opening http://localhost:3000 and trying each evaluation mode!
