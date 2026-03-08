# 🎯 Complete Installation Guide

## Prerequisites

You need these installed BEFORE starting:

### 1. Node.js (Required)
**Download**: https://nodejs.org/en/download/

Choose your platform:
- **Windows**: Download "Windows Installer (.msi)" - 64-bit
- **Mac**: Download "macOS Installer (.pkg)"
- **Linux**: Use package manager or download binary

Verify installation:
```bash
node --version  # Should show v18.x.x or higher
npm --version   # Should show v9.x.x or higher
```

### 2. Python Backend (Already Have)
Make sure your FastAPI backend is working:
```bash
# Test if backend is running
curl http://localhost:8000/health
```

If not running, start it:
```bash
cd d:\D down\bit
python -m uvicorn main_new:app --reload
```

---

## Installation Steps

### Option A: Automated Setup (Windows - Recommended)

1. **Double-click** this file:
   ```
   setup-react-ui.bat
   ```

2. **Wait** for dependencies to install (2-3 minutes first time)

3. **Open browser** to http://localhost:3000

Done! ✅

---

### Option B: Manual Setup (All Platforms)

#### Step 1: Navigate to UI folder
```bash
cd ui-react
```

#### Step 2: Install dependencies
```bash
npm install
```

This will install:
- Next.js (framework)
- React (UI library)
- Tailwind CSS (styling)
- Recharts (charts)
- Framer Motion (animations)
- Lucide React (icons)
- And more...

Expected output:
```
added 350 packages in 2m
```

#### Step 3: Start development server
```bash
npm run dev
```

Expected output:
```
ready - started server on 0.0.0.0:3000
url: http://localhost:3000
```

#### Step 4: Open in browser
Navigate to: **http://localhost:3000**

---

## First Time Experience

When you open the app, you'll see:

1. **Homepage** with:
   - Animated hero section
   - Feature showcase cards
   - Live statistics
   - Quick action buttons

2. **Click "Start Evaluating"** to go to upload page

3. **Upload test files**:
   - Click or drag PDF to drop zone
   - Choose Auto or Manual mode
   - Click "Start Evaluation"

4. **View results** with beautiful charts!

---

## Troubleshooting

### Error: "npm is not recognized"
**Solution**: Install Node.js from https://nodejs.org

### Error: "Port 3000 already in use"
**Solution**: 
```bash
# Windows
npx kill-port 3000

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

### Error: "Cannot find module"
**Solution**:
```bash
# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Error: "Build failed"
**Solution**:
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

### Page shows blank
**Solution**:
1. Check browser console (F12)
2. Verify backend is running on port 8000
3. Check for CORS errors

---

## Development Mode vs Production

### Development (What you're running now)
```bash
npm run dev
```
- Hot reload enabled
- Changes reflect instantly
- Larger bundle size
- Debug mode

### Production Build
```bash
npm run build
npm start
```
- Optimized bundle
- Faster performance
- Smaller file sizes
- Production ready

---

## Connecting to Backend

The UI currently uses mock data. To connect to real API:

### 1. Update `ui-react/app/page.tsx`

Add at the top:
```typescript
import axios from 'axios';
```

Create API instance:
```typescript
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});
```

### 2. Replace Mock Function

Find this function:
```typescript
const handleEvaluate = async () => {
  setIsProcessing(true);
  // ... mock code
};
```

Replace with:
```typescript
const handleEvaluate = async () => {
  setIsProcessing(true);
  try {
    const formData = new FormData();
    formData.append('answer_sheet', answerFile);
    formData.append('question_paper', questionFile);
    
    const endpoint = evaluationMode === 'auto' 
      ? '/evaluate/pdf-auto' 
      : '/evaluate/pdf';
    
    const response = await api.post(endpoint, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    setResult(response.data);
    setActiveTab('results');
  } catch (error) {
    console.error('Evaluation failed:', error);
    alert('Failed to evaluate. Please try again.');
  } finally {
    setIsProcessing(false);
  }
};
```

### 3. Test Connection

1. Make sure backend is running on port 8000
2. Upload real PDF files
3. Click evaluate
4. Should see real results from API!

---

## Customization Guide

### Change Brand Color

Edit `ui-react/tailwind.config.js`:
```javascript
colors: {
  primary: {
    500: '#FF6B6B', // Your brand color
    600: '#EE5A52', // Darker shade
  }
}
```

### Change Font

Edit `ui-react/app/layout.tsx`:
```typescript
// Available fonts: Inter, Roboto, Poppins, etc.
import { Poppins } from 'next/font/google'
const poppins = Poppins({ 
  weight: ['400', '700'],
  subsets: ['latin'] 
})
```

### Add Logo

1. Put logo in `ui-react/public/logo.png`
2. Update navigation in `page.tsx`:
```tsx
<img src="/logo.png" alt="Logo" className="w-12 h-12" />
```

---

## Performance Tips

### 1. Enable Compression
Add to backend (`main_new.py`):
```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 2. Optimize Images
Use Next.js Image component:
```typescript
import Image from 'next/image'
<Image src="/logo.png" width={100} height={100} alt="Logo" />
```

### 3. Lazy Load Components
```typescript
import dynamic from 'next/dynamic'
const Chart = dynamic(() => import('./Chart'), { ssr: false })
```

---

## Deployment Options

### Vercel (Easiest)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Netlify
```bash
# Build
npm run build

# Drag _next folder to Netlify drop
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## File Structure Reference

```
ui-react/
├── app/                    # App router pages
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx          # Main page
├── public/                # Static assets
├── package.json          # Dependencies
├── tailwind.config.js    # Tailwind config
├── tsconfig.json        # TypeScript config
└── postcss.config.js    # PostCSS config
```

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server |
| `npm run build` | Build for production |
| `npm start` | Run production build |
| `npm run lint` | Check code quality |

---

## Support Resources

- **Next.js Docs**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Recharts**: https://recharts.org
- **Framer Motion**: https://www.framer.com/motion/

---

## Quick Checklist

Before opening an issue, check:

- [ ] Node.js 18+ installed
- [ ] Backend running on port 8000
- [ ] Dependencies installed (`npm install`)
- [ ] No errors in terminal
- [ ] Browser console clear (F12)
- [ ] Correct Node version

---

## Success Indicators

You know it's working when:

✅ Terminal shows: `ready - started server on 0.0.0.0:3000`  
✅ Browser opens to animated homepage  
✅ No console errors (F12)  
✅ Buttons have hover effects  
✅ Charts render smoothly  

---

**Need help?** Check these files:
- `README.md` - Full documentation
- `QUICK_START_REACT.md` - Quick start guide
- `UI_TRANSFORMATION_SUMMARY.md` - What changed

**Ready?** Run `setup-react-ui.bat` and enjoy! 🚀
