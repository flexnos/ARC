# 🎯 Demo Mode - Complete Guide

## ✨ What is Demo Mode?

**Demo Mode** lets you test ALL UI features **WITHOUT** needing to connect to the backend API! Perfect for:
- Testing the UI offline
- Showing demos to others
- Development without backend dependencies
- Quick feature exploration

---

## 🚀 How to Use Demo Mode

### Step 1: Enable Demo Mode

1. Open http://localhost:3001
2. Click **"Text"** tab (or Advanced tab)
3. Look for the toggle switch at the top:
   ```
   Backend Mode 🔴 [Toggle] 🟢 DEMO :Demo Mode
   ```
4. Toggle it to **"DEMO"** mode
5. You'll see a purple badge: "✨ No backend needed"

### Step 2: Evaluate in Demo Mode

**Text Mode:**
1. Enable Demo Mode toggle
2. Optionally enter your own question/student answer
3. Select "Auto Reference" or "Manual Reference"
4. Toggle CNN option if desired
5. Click "Evaluate Answer"
6. **Instant results with simulated data!**

**Advanced Mode:**
1. Enable Demo Mode toggle  
2. Upload PDFs (optional - demo works without)
3. Select Auto/Manual reference
4. Toggle CNN option
5. Click "Evaluate"
6. **See results immediately!**

---

## 📊 What Demo Mode Shows

### Mock Results Include:
- **Score:** 8.7/10
- **Grade:** A
- **Percentage:** 87%
- **Metrics:**
  - Similarity: 89%
  - Coverage: 82%
  - Grammar: 94%
  - Relevance: 86%
  - CNN Score: 85% (if enabled)

### Sample Content:
```
Question: "Explain the process of photosynthesis in plants."

Student Answer: "Photosynthesis is how plants make their own food using 
sunlight, water, and carbon dioxide. They convert light energy into 
chemical energy stored in glucose."

AI Reference Answer: "Photosynthesis is the biochemical process by which 
green plants convert light energy into chemical energy. Using chlorophyll, 
they absorb sunlight and combine carbon dioxide from the air with water 
to produce glucose and oxygen..."
```

---

## 🎨 Visual Indicators

### When Demo Mode is Active:

1. **Toggle Area:**
   - Green badge when LIVE (backend connected)
   - Purple badge when DEMO (offline)

2. **Results Page:**
   - Green banner at top: "✅ Demo Mode Active"
   - Message: "This is simulated data. Connect backend for real evaluation."
   - Button: "Switch to Live Mode"

3. **HTML Report:**
   - Downloadable report includes all mock data
   - Beautiful formatting with all metrics
   - AI Reference Answer shown in purple box

---

## 🔄 Switching Between Modes

### Demo → Live:
1. Click "Switch to Live Mode" button on results page
   OR
2. Toggle the switch back to "LIVE"
3. Make sure backend is running on http://localhost:8000
4. Evaluate will now call real API

### Live → Demo:
1. Toggle switch to "DEMO"
2. No backend needed!
3. Instant results every time

---

## 💡 Pro Tips

1. **Quick Testing:** Use Demo mode to quickly test UI changes without starting backend

2. **Presentations:** Demo mode is perfect for showing off the UI without worrying about backend errors

3. **Development:** Develop frontend features independently from backend

4. **Comparison:** Test both modes to see the difference between mock and real data

5. **CNN Feature:** Demo mode shows what CNN scoring would look like (85% score) even if the actual CNN model isn't loading

---

## 🛠️ Technical Details

### How It Works:

```typescript
// In handleEvaluate function:
if (demoMode) {
  // Skip API call
  await setTimeout(1500); // Simulate network delay
  
  const mockResult: Result = {
    score: 8.7,
    grade: 'A',
    // ... all other fields
  };
  
  setResult(mockResult);
  setActiveTab('results);
  return;
}

// Normal mode calls backend
const response = await fetch(`${API_BASE}/evaluate...`);
```

### Demo Mode Data Flow:
```
User clicks Evaluate
     ↓
Check if demoMode === true
     ↓
YES: Use mock data → Show results (1.5s delay)
NO: Call backend API → Wait for response → Show results
```

---

## ✅ Features Available in Demo Mode

### ✅ Working:
- All UI tabs (Text, Advanced, OCR, Batch)
- CNN toggle option
- AI Scoring Options collapsible section
- Manual/Auto reference switching
- Result display with all metrics
- HTML report generation
- Grade badges and score circles
- Radar charts and visualizations
- AI Reference Answer display
- Student Answer display
- Question display

### ⚠️ Limitations:
- Results are pre-defined (not dynamic)
- Same mock data every time (unless you modify inputs)
- No actual ML/AI processing
- No PDF extraction (in Advanced mode)
- No real-time feedback

---

## 🎯 Use Cases

### 1. **UI Testing**
```
Developer wants to test new CSS styles
→ Enable Demo Mode
→ Get instant results
→ See changes immediately
```

### 2. **Feature Demos**
```
Showing the app to stakeholders
→ No backend setup needed
→ Professional-looking results
→ Smooth presentation
```

### 3. **Offline Development**
```
Working from home without server access
→ Demo mode keeps you productive
→ Test UI logic
→ Build new features
```

### 4. **Education**
```
Teaching how the system works
→ Show input/output flow
→ Explain evaluation metrics
→ Demonstrate AI capabilities
```

---

## 🔮 Future Enhancements

Potential improvements:
- Multiple demo scenarios (excellent/poor answers)
- Customizable mock data
- Randomized scores for variety
- Different subject examples
- Multi-language demos

---

## 📝 Summary

**Demo Mode = Freedom from Backend Dependencies**

- ✅ Toggle on/off anytime
- ✅ Works completely offline
- ✅ Shows all UI features
- ✅ Generates downloadable reports
- ✅ Perfect for testing & demos

**Try it now:**
1. Go to Text tab
2. Toggle to DEMO mode
3. Click Evaluate
4. See the magic! ✨

---

**Created:** 2026-03-16  
**Last Updated:** 2026-03-16  
**Status:** ✅ Fully Functional
