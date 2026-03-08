# 🎓 ARC - AI Answer Evaluation System

Professional AI-powered subjective answer evaluation system with modern React UI.

## ✨ Features

- **Auto Reference Generation** - AI generates reference answers from questions
- **PDF Processing** - Extract and evaluate answers from PDFs automatically  
- **Smart Scoring** - Multi-dimensional evaluation (Similarity, Coverage, Grammar, Relevance)
- **Professional UI** - Modern React/Next.js interface with beautiful animations
- **Instant Feedback** - Get detailed scoring in seconds
- **Analytics Dashboard** - Interactive charts and progress tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+

### 1. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies
```bash
cd ui-react
npm install
```

### 3. Start Backend Server
```bash
# Terminal 1
python app.py
```

### 4. Start Frontend UI
```bash
# Terminal 2
cd ui-react
npm run dev
```

### 5. Open Browser
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
bit/
├── main.py                 # FastAPI backend
├── app.py                  # Entry point
├── ui-react/              # React frontend
│   ├── app/page.tsx       # Main UI component
│   └── ...                # React app files
├── config.py              # Configuration
├── security.py            # Security & validation
├── models.py              # ML model management
├── scoring.py             # Scoring algorithms
├── database.py            # Database operations
├── pdf_processor.py       # PDF processing
├── auto_ref_generator.py  # Auto-reference generation
└── requirements.txt       # Python dependencies
```

## 🎯 Usage

### Evaluate Answers via UI
1. Open http://localhost:3000
2. Click "Evaluate" in navigation
3. Upload answer sheet PDF
4. Upload question paper PDF
5. Choose Auto or Manual reference mode
6. Click "Start Evaluation"
7. View results with beautiful charts!

### Evaluate via API
```python
import requests

# Auto-reference evaluation
files = {
    'answer_sheet': open('student_answers.pdf', 'rb'),
    'question_paper': open('questions.pdf', 'rb')
}
data = {'student_name': 'John Doe'}

response = requests.post(
    'http://localhost:8000/evaluate/pdf-auto',
    files=files,
    data=data
)
print(response.json())
```

## 🔧 Configuration

Create `.env` file in root directory:
```env
# Backend Configuration
BACKEND_URL=http://127.0.0.1:8000
HOST=127.0.0.1
PORT=8000

# Model Configuration
DEFAULT_MODEL=MiniLM

# Security (Optional)
API_KEY=your-secret-key-here
RATE_LIMIT_REQUESTS=100

# Database
DATABASE_URL=sqlite:///./evaluations.db
```

## 🎨 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Sentence Transformers** - Semantic similarity
- **PyMuPDF** - PDF processing
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation

### Frontend
- **Next.js 14** - React framework
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **TypeScript** - Type safety

## 📊 Features Breakdown

### Auto Reference Mode
- AI generates reference answers from questions
- Only requires answer sheet + question paper
- Perfect for quick evaluations
- Uses NLP to understand question context

### Manual Reference Mode
- Traditional evaluation with provided references
- Requires answer sheet + question paper + reference answers
- More accurate when references are available

### Scoring Metrics
1. **Semantic Similarity** (40%) - How close to reference answer
2. **Content Coverage** (30%) - Keyword coverage from reference
3. **Grammar Quality** (15%) - Sentence structure and grammar
4. **Relevance** (15%) - How relevant to the question

### Analytics Dashboard
- **Radar Chart** - Multi-metric visualization
- **Score Progression** - Track improvement over time
- **Grade Distribution** - See performance breakdown
- **Detailed Feedback** - AI-generated suggestions

## 🔒 Security

- API key authentication (optional)
- Rate limiting per IP
- File size validation
- File type validation
- Input sanitization
- CORS protection

## 📈 Performance

- **Load Time**: <1 second
- **Bundle Size**: ~180KB
- **Evaluation Speed**: 2-3 seconds per PDF
- **Concurrent Users**: Supports 100+ users

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
cd ui-react
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
```bash
# Kill process on port 8000 or 3000
npx kill-port 8000
npx kill-port 3000
```

## 📝 API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /evaluate` - Evaluate single answer
- `POST /evaluate/pdf-auto` - Evaluate PDFs with auto-reference
- `POST /evaluate/pdf` - Evaluate PDFs with manual reference
- `GET /models` - List available models
- `GET /statistics` - Get evaluation statistics

## 🎓 Documentation

- **UI Guide**: `ui-react/README.md`
- **Quick Start**: `QUICK_START_REACT.md`
- **Installation**: `INSTALLATION_GUIDE.md`
- **API Docs**: http://localhost:8000/docs

## 📄 License

MIT License - Feel free to use in your projects!

## 🤝 Support

For issues or questions:
1. Check documentation files
2. Review API docs at /docs
3. Check console for errors
4. Verify both backend and frontend are running

---

**Built with ❤️ using FastAPI and Next.js**
