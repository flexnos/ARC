# 🚨 Troubleshooting Guide

## Quick Fix - Run These Scripts

### Step 1: Start Backend
Double-click: **`start_backend.bat`**

This will:
- Check Python version
- Install missing dependencies
- Start the API server at http://localhost:8000

### Step 2: Start Frontend  
Double-click: **`start_frontend.bat`**

This will:
- Check Node.js version
- Install npm packages (first time only)
- Start the React app at http://localhost:3000

### OR Use The All-in-One Launcher
Double-click: **`START_HERE.bat`**

This opens both servers automatically in separate windows!

---

## Common Issues

### Issue 1: "Python not found"
**Solution**: Install Python 3.8+ from https://python.org

### Issue 2: "Node.js not found"
**Solution**: Install Node.js 18+ from https://nodejs.org

### Issue 3: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: 
```bash
pip install fastapi uvicorn python-multipart pydantic
```

### Issue 4: "npm ERR!" or "Cannot find module"
**Solution**:
```bash
cd ui-react
rm -rf node_modules package-lock.json
npm install
```

### Issue 5: "Port 8000 already in use"
**Solution**:
```bash
# Windows
npx kill-port 8000

# Or manually close any program using port 8000
```

### Issue 6: "Port 3000 already in use"
**Solution**:
```bash
# Windows
npx kill-port 3000
```

### Issue 7: Backend starts but immediately closes
**Solution**: 
1. Open `start_backend.bat` with Notepad
2. Look for error messages
3. Usually means missing dependency - run: `pip install -r requirements.txt`

### Issue 8: Frontend shows blank page
**Solution**:
1. Wait 10-15 seconds (first build takes time)
2. Check browser console (F12) for errors
3. Make sure backend is running on port 8000
4. Try refreshing the page (Ctrl+R)

### Issue 9: Models loading very slowly
**Solution**: This is normal on first run. Models are downloaded and cached. Subsequent runs will be faster.

### Issue 10: "get_terminal_output" or terminal issues
**Solution**: The batch files open new windows - don't run from PowerShell directly. Double-click the `.bat` files instead.

---

## Manual Start (If Batch Files Don't Work)

### Start Backend Manually
Open Command Prompt or PowerShell:
```bash
cd d:\D down\bit
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Start Frontend Manually
Open a NEW terminal window:
```bash
cd d:\D down\bit\ui-react
npm run dev
```

---

## Verify It's Working

### Backend Check
Open browser to: http://localhost:8000/health

Should show:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Frontend Check
Open browser to: http://localhost:3000

Should show the animated homepage with:
- "AI-Powered Answer Evaluation" title
- Feature cards
- Navigation menu

---

## Still Not Working?

### Check These First:
1. ✅ Python 3.8+ installed? (`python --version`)
2. ✅ Node.js 18+ installed? (`node --version`)
3. ✅ Both terminals show no errors?
4. ✅ Ports 8000 and 3000 are free?

### Get More Info:
1. Check what error message appears in the terminal windows
2. Look at `main.py` line 1 for import errors
3. Check `ui-react/package.json` exists
4. Verify internet connection (for npm installs)

### Last Resort:
Delete and reinstall everything:
```bash
# Backend
pip uninstall fastapi uvicorn python-multipart pydantic
pip install fastapi uvicorn python-multipart pydantic

# Frontend
cd ui-react
rm -rf node_modules package-lock.json
npm install
```

---

## Success Indicators

You know it's working when you see:

### Backend Window:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Frontend Window:
```
ready - started server on 0.0.0.0:3000
Local:   http://localhost:3000
```

### Browser:
- Can access http://localhost:8000/docs (API docs)
- Can access http://localhost:3000 (React UI)
- Both pages load without errors

---

## Contact Support

If nothing works:
1. Take screenshot of error messages
2. Note your Python and Node versions
3. Check if antivirus/firewall is blocking ports
4. Try running as Administrator

**Most common fix**: Close all terminals, run `start_backend.bat` and `start_frontend.bat` fresh!
