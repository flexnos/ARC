# 🚨 URGENT FIX NEEDED!

## The Problem
The frontend `node_modules` folder is missing! This means npm packages were never installed.

## ✅ THE FIX - Run This ONCE

### Step 1: Install Frontend Dependencies
Open PowerShell or Command Prompt and run:

```bash
cd "d:\D down\bit\ui-react"
npm install
```

**This will take 2-3 minutes** on first run (downloads ~350 packages).

Wait until you see:
```
added 350 packages in 2m
```

### Step 2: Verify Installation
Check that `node_modules` folder now exists in `ui-react/` directory.

### Step 3: Start Servers
NOW you can use the batch files:
- Double-click `START_HERE.bat`, OR
- Run `start_backend.bat` and `start_frontend.bat` separately

---

## 📋 Complete Setup Checklist

Do these IN ORDER:

### 1. Check Prerequisites
```bash
python --version    # Should be 3.8+
node --version      # Should be 18+
npm --version       # Should be 9+
```

### 2. Install Backend Dependencies (if not done)
```bash
cd "d:\D down\bit"
pip install fastapi uvicorn python-multipart pydantic sentence-transformers
```

### 3. Install Frontend Dependencies (CRITICAL!)
```bash
cd "d:\D down\bit\ui-react"
npm install
```

**WAIT for this to complete!** You'll see:
- Progress bar
- Package downloads
- "added XXX packages" message

### 4. Start Backend
Double-click: `start_backend.bat`

Should show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 5. Start Frontend  
Double-click: `start_frontend.bat`

Should show:
```
ready - started server on 0.0.0.0:3000
```

### 6. Open Browser
Go to: http://localhost:3000

---

## ⚡ Quick Install Commands

Copy-paste these one at a time:

### Backend Install:
```powershell
cd "d:\D down\bit"
pip install fastapi uvicorn python-multipart pydantic sentence-transformers fuzzywuzzy python-Levenshtein PyMuPDF pytesseract Pillow sqlalchemy pandas plotly streamlit python-dotenv
```

### Frontend Install:
```powershell
cd "d:\D down\bit\ui-react"
npm install
```

---

## ❓ How to Know It Worked?

### Backend Success:
- Terminal shows "Application startup complete"
- Can open http://localhost:8000/health in browser
- Shows JSON with status: "healthy"

### Frontend Success:
- Terminal shows "ready - started server"  
- Can open http://localhost:3000 in browser
- Shows animated React UI (not blank page!)

---

## 🔴 If npm install Fails

### Error: "network timeout"
```bash
npm config set registry https://registry.npmjs.org/
npm install
```

### Error: "EACCES permission denied"
Run terminal as Administrator, then:
```bash
npm install
```

### Error: "No matching version found"
Delete package-lock.json and try again:
```bash
rm package-lock.json
npm install
```

### Still failing?
Try cleaning npm cache:
```bash
npm cache clean --force
npm install
```

---

## 💡 Pro Tip

**First-time npm install takes 2-5 minutes.** Be patient! You'll see:
1. Downloading packages...
2. Extracting...
3. Building...
4. "added 350 packages in 2m"

After first install, subsequent starts are instant!

---

## ✅ Final Test

After npm install completes:

1. Run `start_backend.bat` ✓
2. Run `start_frontend.bat` ✓  
3. Open http://localhost:3000 ✓
4. See beautiful UI! ✓

**If you see the UI - YOU DID IT!** 🎉

---

**REMEMBER**: You only need to run `npm install` ONCE. After that, just use the batch files!
