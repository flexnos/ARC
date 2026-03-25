# How to See the New Features - Visual Guide

## 🚀 Quick Start

### 1. Open the App

**URL:** http://localhost:3001

You should see the main page with tabs at the top.

---

## 📍 Where to Look for CNN Toggle

### Step 1: Click "Text" Tab

```
[Home] [Text] [Advanced] [OCR] [Batch] [Results]
        ↑
     Click here first
```

### Step 2: Scroll Down

Below the question and answer text boxes, you'll see:

```
┌─────────────────────────────────────┐
│ Question                            │
│ [text box...]                       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Student Answer                      │
│ [text box...]                       │
└─────────────────────────────────────┘

┌──────────────────┬──────────────────┐
│ 🤖 Auto Reference│ 📝 Manual Ref    │
└──────────────────┴──────────────────┘

┌─────────────────────────────────────┐
│ 🧠 AI Scoring Options          ›   │  ← LOOK HERE!
└─────────────────────────────────────┘
       ↑
   This is the new button!
```

### Step 3: Click "AI Scoring Options"

Click the button labeled **"AI Scoring Options"** and it will expand to show:

```
┌─────────────────────────────────────┐
│ ✨ CNN Deep Learning         [⚪]   │
│ Enable hybrid scoring with CNN +   │
│ Transformers for enhanced accuracy │
│                                     │
│ ⚡ Hybrid mode enabled: 40% CNN +  │
│    60% Transformer scoring          │
└─────────────────────────────────────┘
```

### Step 4: Toggle CNN ON

Click the toggle switch on the right side to enable CNN scoring!

---

## 📊 Where to See Generated Reference Answers

### After You Evaluate

When you click "Evaluate Answer", the results will show:

### Location 1: Performance Overview Card

At the very TOP of the results (before the score):

```
┌─────────────────────────────────────┐
│ ✨ AI-Generated Reference Answer    │  ← BADGE
│ This reference was automatically   │
│ generated from the question using  │
│ AI                                  │
└─────────────────────────────────────┘

Score: 8.5/10
Grade: A
```

### Location 2: Detailed Analysis Section

Scroll down in the results page to find:

```
Detailed Analysis
═════════════════════════════════════

📄 Question
[The question you entered]

✨ AI Reference Answer (Auto-Generated)  ← PURPLE BOX
[Purple background box showing the AI-generated reference]

✓ Student Answer
[Green background box showing student's answer]

Semantic Similarity    ████████░░ 80%
Content Coverage       ███████░░░ 70%
Grammar Quality        █████████░ 90%
Relevance              ████████░░ 80%
CNN Deep Learning      ███████░░░ 70%  ← If CNN enabled
```

---

## 🎯 Complete Test Walkthrough

### Let's Test It Together!

**Step 1:** Open http://localhost:3001

**Step 2:** Click "Text" tab (top navigation)

**Step 3:** Fill in the form:
```
Question: "What is photosynthesis?"

Student Answer: 
"Photosynthesis is how plants make food using sunlight. 
They take carbon dioxide and water, and use light energy 
to create glucose and oxygen."

Mode: Select "Auto Reference"
```

**Step 4:** Look for "AI Scoring Options" button
- It's RIGHT BELOW the mode selection buttons
- Has a brain icon (🧠)
- Says "AI Scoring Options"

**Step 5:** Click it to expand
- Should reveal CNN toggle
- Purple sparkle icon appears
- Toggle switch on the right

**Step 6:** Toggle CNN ON (optional)
- Click the switch
- Purple info badge appears below

**Step 7:** Click "Evaluate Answer"

**Step 8:** View Results
- **Look at TOP** → See "AI-Generated Reference Answer" badge
- **Look at score** → See your evaluation
- **Scroll down** → See detailed analysis
- **Look for purple box** → "AI Reference Answer (Auto-Generated)"
- **See the reference text** displayed in the purple box

---

## 🔍 Troubleshooting

### Can't See CNN Toggle?

**Check:**
1. ✅ Are you in "Text" tab? (Only shows there)
2. ✅ Did you scroll down? (Below mode buttons)
3. ✅ Is the button visible? Look for brain icon
4. ✅ Did you click to expand? (It's collapsible)

**Button looks like this:**
```
┌─────────────────────────────────┐
│ 🧠 AI Scoring Options       ›   │
└─────────────────────────────────┘
```

### Can't See Reference Answer?

**Requirements:**
1. ✅ Must use "Auto Reference" mode
2. ✅ Must complete evaluation
3. ✅ Backend must be running (port 8000)

**Check backend:**
- Should be running on http://localhost:8000
- Check terminal for errors
- Look for "Loaded sentence transformer" messages

### Page Not Loading?

**Try:**
```bash
# Stop current server (Ctrl+C)
# Then restart:
cd ui-react
npm run dev
```

---

## 📱 What You Should See

### Full Page Layout

```
╔═══════════════════════════════════════════╗
║  [Logo]  Home Text Advanced OCR Batch     ║
╠═══════════════════════════════════════════╣
║                                           ║
║  Text-Based Analysis                      ║
║  Paste student and reference answers      ║
║                                           ║
║  ┌─────────────────────────────────────┐ ║
║  │ Question                            │ ║
║  │ [_______________________________]   │ ║
║  └─────────────────────────────────────┘ ║
║                                           ║
║  ┌─────────────────────────────────────┐ ║
║  │ Student Answer                      │ ║
║  │ [_______________________________]   │ ║
║  │                                     │ ║
║  │                                     │ ║
║  └─────────────────────────────────────┘ ║
║                                           ║
║  ┌──────────────┐ ┌──────────────┐       ║
║  │ 🤖 Auto      │ │ 📝 Manual    │       ║
║  │  Reference   │ │  Reference   │       ║
║  └──────────────┘ └──────────────┘       ║
║                                           ║
║  ┌─────────────────────────────────────┐ ║
║  │ 🧠 AI Scoring Options           ›   │ ║ ← NEW!
║  └─────────────────────────────────────┘ ║
║                                           ║
║  ┌─────────────────────────────────────┐ ║
║  │      [ Evaluate Answer ]            │ ║
║  └─────────────────────────────────────┘ ║
║                                           ║
╚═══════════════════════════════════════════╝
```

### After Evaluation - Results

```
╔═══════════════════════════════════════════╗
║  Download HTML Report                     ║
╠═══════════════════════════════════════════╣
║  PERFORMANCE OVERVIEW                     ║
║                                           ║
║  ┌─────────────────────────────────────┐ ║
║  │ ✨ AI-Generated Reference Answer    │ ║ ← NEW!
║  └─────────────────────────────────────┘ ║
║                                           ║
║         Score: 8.5/10                     ║
║         Grade: A                          ║
║                                           ║
║         [Radar Chart]                     ║
║                                           ║
╠═══════════════════════════════════════════╣
║  DETAILED ANALYSIS                        ║
║                                           ║
║  📄 Question                              ║
║  [Question text]                          ║
║                                           ║
║  ✨ AI Reference Answer (Auto-Generated)  ║ ← NEW!
║  ┌─────────────────────────────────────┐ ║
║  │ [Purple box with reference text]    │ ║
║  └─────────────────────────────────────┘ ║
║                                           ║
║  ✓ Student Answer                         ║
║  ┌─────────────────────────────────────┐ ║
║  │ [Green box with student text]       │ ║
║  └─────────────────────────────────────┘ ║
║                                           ║
║  Metrics:                                 ║
║  Semantic Similarity    80%              ║
║  Content Coverage       70%              ║
║  Grammar Quality        90%              ║
║  Relevance              80%              ║
║  CNN Deep Learning      70% (if enabled) ║ ← NEW!
║                                           ║
║  AI Feedback:                             ║
║  [Feedback text]                          ║
╚═══════════════════════════════════════════╝
```

---

## ✅ Checklist

Before you start, make sure:

- [ ] Backend is running on http://localhost:8000
- [ ] Frontend is running on http://localhost:3001
- [ ] You're in the "Text" tab
- [ ] You've scrolled down to see all options

Features to look for:

- [ ] "AI Scoring Options" button (with brain icon)
- [ ] Expandable section when clicked
- [ ] CNN toggle inside expanded section
- [ ] Purple gradient toggle switch
- [ ] After evaluation: AI badge at top
- [ ] After evaluation: Purple reference box in details

---

## 🎨 Color Guide

**CNN Toggle:**
- OFF: Gray/white switch
- ON: Purple to pink gradient

**Reference Answer Box:**
- Background: Light purple (purple-500/10)
- Border: Purple outline (purple-500/20)
- Header: Purple text (purple-300)
- Icon: Sparkles (purple-400)

**Badge:**
- Gradient: Purple to pink
- Premium appearance

---

## 💡 Quick Tips

1. **CNN Toggle is COLLAPSIBLE** - Must click "AI Scoring Options" first
2. **Located under mode buttons** - Scroll down past Auto/Manual selection
3. **Only in Text mode** - Won't show in other tabs
4. **Reference shows AFTER evaluation** - Not visible before submitting
5. **Purple = AI generated** - Color coding throughout UI

---

## 🆘 Still Can't See It?

**Send me:**
1. Screenshot of what you see
2. Which tab you're on
3. Whether backend is running
4. Any error messages in console

I'll help you locate the features! 

---

## 🎯 Expected Browser View

Open browser console (F12) and check:
- No JavaScript errors
- Network tab shows requests to localhost:8000
- React components loading properly

**Normal console messages:**
```
✓ Compiled successfully
Ready in 3.5s
```

**If you see errors**, share them with me!

---

Let me know which specific feature you can't see, and I'll help you find it! 😊
