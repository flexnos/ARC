# CNN Toggle - Visual Guide

## 🎨 What You'll See

### 1. AI Scoring Options Button (Collapsed)

When you're in Text evaluation mode, you'll see a new button below the evaluation mode selectors:

```
┌──────────────────────────────────────────────┐
│  🧠 AI Scoring Options                  ›    │
└──────────────────────────────────────────────┘
```

**Features:**
- Brain icon (🧠) indicates AI functionality
- Clean, minimal design
- Right arrow (›) indicates expandable
- Hover effect with subtle glow

---

### 2. Expanded AI Scoring Options

Click the button to reveal:

```
┌──────────────────────────────────────────────┐
│  🧠 AI Scoring Options                  ‹    │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ ✨ CNN Deep Learning          [⚪]      │ │
│  │ Enable hybrid scoring with CNN +       │ │
│  │ Transformers for enhanced accuracy     │ │
│  └────────────────────────────────────────┘ │
│                                              │
└──────────────────────────────────────────────┘
```

**Features:**
- Smooth expand animation
- Purple sparkle icon (✨) for CNN
- Toggle switch on the right (OFF state shown as ⚪)
- Description text below title

---

### 3. CNN Toggle ON (Enabled)

Flip the toggle to enable CNN:

```
┌──────────────────────────────────────────────┐
│  ✨ CNN Deep Learning          [🟣━━━●]     │
│  Enable hybrid scoring with CNN +           │
│  Transformers for enhanced accuracy         │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ ⚡ Hybrid mode enabled: 40% CNN +     │  │
│  │    60% Transformer scoring            │  │
│  └───────────────────────────────────────┘  │
│                                             │
└──────────────────────────────────────────────┘
```

**Visual Changes:**
- Toggle slides to right with gradient (purple → pink)
- Info badge appears below with purple background
- Lightning bolt icon (⚡) indicates active feature
- Shows exact weighting (40% CNN + 60% Transformer)

---

### 4. Evaluation Results (Without CNN)

Standard metrics display:

```
Metrics Breakdown:

Semantic Similarity    ████████░░ 80%
Content Coverage       ███████░░░ 70%
Grammar Quality        █████████░ 90%
Relevance              ████████░░ 80%
```

**Colors:**
- Blue gradient for Similarity
- Purple/pink for Coverage
- Green for Grammar
- Yellow/orange for Relevance

---

### 5. Evaluation Results (With CNN)

Enhanced metrics with CNN score:

```
Metrics Breakdown:

Semantic Similarity    ████████░░ 80%
Content Coverage       ███████░░░ 70%
Grammar Quality        █████████░ 90%
Relevance              ████████░░ 80%
CNN Deep Learning      ███████░░░ 70% ← NEW!
                       (indigo→purple gradient)
```

**Visual Features:**
- CNN score appears as 5th metric
- Indigo to purple gradient bar
- Matches CNN toggle color scheme
- Clearly labeled "CNN Deep Learning Score"

---

## 🎬 Animation Details

### Toggle Interaction

**OFF → ON:**
1. Toggle slides right (smooth transition)
2. Gradient fills from left to right
3. Info badge fades in and scales up
4. All animations use Framer Motion

**ON → OFF:**
1. Toggle slides left
2. Gradient fades out
3. Info badge shrinks and fades away
4. Returns to minimal state

### Expand/Collapse

**Expand:**
- Height animates from 0 to auto
- Opacity fades in content
- Arrow rotates 90° clockwise
- Duration: ~300ms

**Collapse:**
- Height animates back to 0
- Opacity fades out
- Arrow rotates back
- Smooth easing curve

---

## 📱 Responsive Behavior

### Desktop (> 1024px)

```
┌──────────────────────────────────────────────┐
│  Full width card with centered content       │
│  Toggle positioned on right side             │
│  Text aligned left                           │
└──────────────────────────────────────────────┘
```

### Tablet (768px - 1024px)

```
┌────────────────────────────────────┐
│  Slightly narrower card            │
│  Same layout, adjusted spacing     │
└────────────────────────────────────┘
```

### Mobile (< 768px)

```
┌──────────────────────────┐
│  Compact layout          │
│  Toggle below text       │
│  Stacked vertically      │
└──────────────────────────┘
```

---

## 🎨 Color Palette

### CNN Toggle States

**OFF State:**
- Background: `rgba(255, 255, 255, 0.1)` (white/10)
- Knob: White with gray border
- Border: `rgba(255, 255, 255, 0.1)`

**ON State:**
- Gradient: `linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)`
- Purple (#8b5cf6) → Pink/Purple (#a855f7)
- Knob: Pure white, slides right
- Focus ring: Primary color glow

### CNN Score Bar

**Gradient:**
- Start: Indigo-500 (`#6366f1`)
- End: Purple-500 (`#a855f7`)
- Creates smooth transition

### Info Badge

**Background:**
- `rgba(139, 92, 246, 0.1)` (purple-500/10)
- Border: `rgba(139, 92, 246, 0.3)` (purple-500/30)
- Text: Purple-300 (`#c4b5fd`)

---

## 🖱️ Interactive States

### Button Hover

**AI Scoring Options Button:**
- Default: `bg-white/5`
- Hover: `bg-white/10`
- Border stays consistent
- Text brightens slightly

### Toggle Focus

**Keyboard Navigation:**
- Tab focuses toggle
- Ring appears: `ring-2 ring-primary-500`
- Space/Enter toggles state
- Accessible and keyboard-friendly

### Active State

**While Evaluating:**
- Toggle becomes disabled
- Opacity reduces to 50%
- Loading spinner appears on evaluate button
- User can't change settings mid-evaluation

---

## 📊 Real Example

### Full UI Flow

**Step 1: Open App**
```
[Home] [Text] [Advanced] [OCR] [Batch] [Results]
                                        ↑
                                   Click here
```

**Step 2: Text Mode**
```
Question: [________________________]
Student Answer: [_________________]
              
[Auto Reference] [Manual Reference]

🧠 AI Scoring Options ›
              
[Evaluate Answer]
```

**Step 3: Expand Options**
```
[Auto Reference] [Manual Reference]

🧠 AI Scoring Options ‹
┌────────────────────────────┐
│ ✨ CNN Deep Learning [⚪]  │
│ Enable hybrid scoring...   │
└────────────────────────────┘

[Evaluate Answer]
```

**Step 4: Enable CNN**
```
[Auto Reference] [Manual Reference]

🧠 AI Scoring Options ‹
┌────────────────────────────┐
│ ✨ CNN Deep Learning [🟣]  │
│ Enable hybrid scoring...   │
│                            │
│ ⚡ Hybrid mode: 40% CNN +  │
│    60% Transformer         │
└────────────────────────────┘

[Evaluate Answer]
```

**Step 5: Results**
```
Score: 8.7/10 | Grade: A

Metrics:
████████░░ Semantic Similarity 80%
███████░░░ Content Coverage 70%
█████████░ Grammar Quality 90%
████████░░ Relevance 80%
███████░░░ CNN Deep Learning 70% ← NEW!

AI Feedback: Excellent answer! ...
```

---

## 🎯 Key Design Principles

### 1. Progressive Disclosure
- Advanced options hidden by default
- User chooses when to see complexity
- Keeps interface clean and simple

### 2. Visual Hierarchy
- CNN toggle uses purple (premium color)
- Gradient indicates special feature
- Info badge provides immediate feedback

### 3. Consistency
- Matches existing design system
- Uses same animation patterns
- Follows React component structure

### 4. Accessibility
- High contrast colors
- Clear focus indicators
- Keyboard navigable
- Screen reader friendly labels

### 5. Performance
- Hardware-accelerated animations
- Minimal re-renders
- Smooth 60fps transitions

---

## 💡 Tips & Best Practices

### For Users

✅ **Best Results:**
- Use CNN for complex, subjective answers
- Enable for final grading decisions
- Compare with/without CNN for borderline cases

❌ **When Not Needed:**
- Simple factual questions
- Quick practice evaluations
- When speed is priority

### For Developers

✅ **Implementation:**
- Keep state close to where it's used
- Use conditional rendering for performance
- Animate opacity AND height together

❌ **Avoid:**
- Don't show CNN option everywhere
- Don't force users to enable it
- Don't hide important info in collapsed section

---

## 🎉 Summary

The CNN toggle is designed to be:

✅ **Beautiful** - Premium gradient design  
✅ **Intuitive** - Clear on/off states  
✅ **Informative** - Shows exact weighting  
✅ **Accessible** - Works for everyone  
✅ **Performant** - Smooth animations  

It seamlessly integrates into the existing UI while standing out as a premium feature for enhanced AI scoring.

**Ready to use!** 🚀
