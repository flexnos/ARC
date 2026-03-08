# 🖥️ MANUAL APPROACH - No Double-Clicking!

## Choose ONE of these methods:

---

## ⚡ METHOD 1: Run PowerShell Script (Easiest!)

### Just run this ONE command in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File "d:\D down\bit\SETUP_MANUAL.ps1"
```

**What it does:**
1. ✅ Checks Node.js is installed
2. ✅ Navigates to correct folders
3. ✅ Installs npm packages (if needed)
4. ✅ Starts backend server
5. ✅ Starts frontend UI
6. ✅ Opens browser automatically

**All steps happen automatically!** ✨

---

## 📝 METHOD 2: Copy-Paste Commands (Step by Step)

Open PowerShell and run these commands **one by one**:

### Step 1: Open PowerShell
Press `Windows key`, type "PowerShell", press Enter

### Step 2: Navigate to project
```powershell
cd "d:\D down\bit"
```

### Step 3: Check Node.js
```powershell
node --version
```
Should show: `v20.x.x` or similar

### Step 4: Go to ui-react folder
```powershell
cd ui-react
```

### Step 5: Install npm packages (FIRST TIME ONLY)
```powershell
npm install
```
⏱️ Takes 2-5 minutes. Wait for "added XXX packages" message.

### Step 6: Start Backend (in NEW PowerShell window)
Open another PowerShell window, then run:
```powershell
cd "d:\D down\bit"
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Step 7: Start Frontend (in FIRST PowerShell window)
Go back to first window:
```powershell
cd "d:\D down\bit\ui-react"
npm run dev
```

### Step 8: Open Browser
In your browser, go to: http://localhost:3000

---

## 🎯 METHOD 3: Even Simpler - Two Commands

If you want the absolute simplest approach:

### Terminal 1 (Backend):
```powershell
cd "d:\D down\bit"
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Terminal 2 (Frontend):
```powershell
cd "d:\D down\bit\ui-react"
npm install    # ← First time only!
npm run dev    # ← After installation
```

That's it! Two terminals, two commands each.

---

## ✅ What Success Looks Like

### Backend Terminal Shows:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Frontend Terminal Shows:
```
ready - started server on 0.0.0.0:3000
Local:   http://localhost:3000
```

### Browser at http://localhost:3000 Shows:
- Beautiful animated UI
- "AI-Powered Answer Evaluation"
- Navigation menu
- Feature cards

---

## 🔧 If Something Goes Wrong

### Problem: "npm is not recognized"
**Solution:** Install Node.js from https://nodejs.org

### Problem: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
```powershell
cd "d:\D down\bit"
pip install fastapi uvicorn python-multipart pydantic
```

### Problem: "Port already in use"
**Solution:**
```powershell
npx kill-port 8000
npx kill-port 3000
```

---

## 📋 Quick Reference

| What You Want | Command |
|---------------|---------|
| Install frontend packages | `cd ui-react ; npm install` |
| Start backend | `python -m uvicorn main:app --host 127.0.0.1 --port 8000` |
| Start frontend | `cd ui-react ; npm run dev` |
| Do everything automatically | Run `SETUP_MANUAL.ps1` |

---

## 🎯 RECOMMENDED: Use the PowerShell Script

The easiest way is to just run the PowerShell script I created:

```powershell
powershell -ExecutionPolicy Bypass -File "d:\D down\bit\SETUP_MANUAL.ps1"
```

This does ALL the steps automatically and opens both servers for you!

---

**Pick the method that works best for you and copy-paste the commands!** 

No double-clicking needed - just copy, paste, and press Enter! 🎉
