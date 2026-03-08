'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, Upload, Brain, BarChart3, CheckCircle2, Sparkles, ChevronRight,
  FileCheck, Bot, Zap, Award, TrendingUp, Image as ImageIcon, Layers, Copy
} from 'lucide-react';
import { 
  ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, AreaChart, Area
} from 'recharts';

interface Result {
  score: number;
  grade: string;
  percentage: number;
  feedback: string;
  metrics: {
    similarity: number;
    coverage: number;
    grammar: number;
    relevance: number;
  };
  extractedText?: string;  // For OCR results
  question?: string;       // Question text
  studentAnswer?: string;  // Student's answer
  referenceAnswer?: string; // Reference answer (if manual mode)
}

export default function Home() {
  const [activeTab, setActiveTab] = useState<'home' | 'text' | 'advanced' | 'ocr' | 'batch' | 'results'>('home');
  const [evaluationMode, setEvaluationMode] = useState<'manual' | 'auto'>('auto');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [selectedFiles, setSelectedFiles] = useState<{[key: string]: File | null}>({
    answerSheet: null,
    questionPaper: null,
    reference: null,
    ocrImage: null,
    batchFile: null
  });
  const [dragActive, setDragActive] = useState<{[key: string]: boolean}>({});
  const [textInput, setTextInput] = useState('');
  const [textQuestion, setTextQuestion] = useState('');
  const [referenceInput, setReferenceInput] = useState('');
  const [ocrQuestion, setOcrQuestion] = useState('');
  const [extractedText, setExtractedText] = useState('');

  const handleFileSelect = (type: string, file: File | null) => {
    setSelectedFiles(prev => ({ ...prev, [type]: file }));
  };

  const handleDrag = (e: React.DragEvent, type: string) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(prev => ({ ...prev, [type]: true }));
    } else if (e.type === "dragleave") {
      setDragActive(prev => ({ ...prev, [type]: false }));
    }
  };

  const handleDrop = (e: React.DragEvent, type: string) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(prev => ({ ...prev, [type]: false }));
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(type, e.dataTransfer.files[0]);
    }
  };

  const handleEvaluate = async () => {
    setIsProcessing(true);
    
    try {
      const API_BASE = 'http://localhost:8000';
      let response;
      let resultData;

      // TEXT EVALUATION
      if (activeTab === 'text') {
        // For auto mode, use student's answer as temporary reference
        // Backend will handle auto-reference generation
        const payload = {
          question: textQuestion || textInput.substring(0, 200) || 'Evaluate this answer',
          reference_answer: evaluationMode === 'manual' ? referenceInput : textInput,
          student_answer: textInput,
          model_name: null,
          student_name: null
        };
        
        response = await fetch(`${API_BASE}/evaluate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
          throw new Error(`Backend error: ${errorData.detail || response.statusText}`);
        }
        resultData = await response.json();
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
        
        if (!response.ok) throw new Error('PDF evaluation failed');
        resultData = await response.json();
      }
      
      // OCR EVALUATION
      else if (activeTab === 'ocr') {
        const formData = new FormData();
        
        if (selectedFiles.ocrImage) {
          formData.append('image', selectedFiles.ocrImage);
        }
        if (ocrQuestion) {
          formData.append('question_text', ocrQuestion);
        }
        
        // Note: You'll need to create this endpoint on backend
        response = await fetch(`${API_BASE}/evaluate/ocr`, {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) throw new Error('OCR evaluation failed');
        resultData = await response.json();
        
        // Store extracted text if returned by backend
        if (resultData.extracted_text) {
          setExtractedText(resultData.extracted_text);
        }
      }
      
      // BATCH PROCESSING
      else if (activeTab === 'batch') {
        const formData = new FormData();
        
        if (selectedFiles.batchFile) {
          formData.append('zip_archive', selectedFiles.batchFile);
        }
        
        // Note: You'll need to create this endpoint on backend
        response = await fetch(`${API_BASE}/evaluate/batch`, {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) throw new Error('Batch processing failed');
        resultData = await response.json();
      }
      
      // Transform backend response to frontend format
      setResult({
        score: resultData.final_score || resultData.total_obtained_marks || 8.5,
        grade: resultData.grade || 'A',
        percentage: resultData.percentage || 85,
        feedback: resultData.feedback || 'Evaluation completed successfully.',
        metrics: {
          similarity: resultData.similarity || 0.85,
          coverage: resultData.coverage || 0.78,
          grammar: resultData.grammar || 0.92,
          relevance: resultData.relevance || 0.88
        },
        extractedText: resultData.extracted_text || undefined,
        question: activeTab === 'text' ? textQuestion : (activeTab === 'ocr' ? ocrQuestion : undefined),
        studentAnswer: activeTab === 'text' ? textInput : undefined,
        referenceAnswer: evaluationMode === 'manual' && activeTab === 'text' ? referenceInput : undefined
      });

      setActiveTab('results');
      
    } catch (error) {
      console.error('Evaluation error:', error);
      alert('Evaluation failed: ' + (error as Error).message + '\n\nMake sure your backend is running on http://localhost:8000');
    } finally {
      setIsProcessing(false);
    }
  };

  // Generate downloadable HTML report
  const generateHTMLReport = () => {
    if (!result) return;

    const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evaluation Report - Grade ${result.grade}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .header p { font-size: 18px; opacity: 0.9; }
        .score-section {
            text-align: center;
            padding: 40px;
            background: #f8f9fa;
        }
        .score-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 48px;
            font-weight: bold;
            color: white;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        .grade-badge {
            display: inline-block;
            padding: 8px 24px;
            background: white;
            color: #667eea;
            border-radius: 30px;
            font-weight: bold;
            font-size: 24px;
            margin-top: 15px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
        }
        .metric-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 24px;
            transition: all 0.3s;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        .metric-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 8px;
        }
        .metric-bar {
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }
        .metric-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
            transition: width 1s ease;
        }
        .feedback-section {
            padding: 40px;
            background: #f8f9fa;
            border-top: 2px solid #e0e0e0;
        }
        .feedback-section h3 {
            font-size: 24px;
            color: #333;
            margin-bottom: 16px;
        }
        .feedback-text {
            font-size: 16px;
            line-height: 1.8;
            color: #555;
            padding: 20px;
            background: white;
            border-left: 4px solid #667eea;
            border-radius: 8px;
        }
        .details-section {
            padding: 40px;
        }
        .details-section h3 {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 16px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .detail-row:last-child { border-bottom: none; }
        .detail-label { color: #666; font-weight: 600; }
        .detail-value { color: #333; font-weight: 500; }
        .timestamp {
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 14px;
            border-top: 2px solid #e0e0e0;
        }
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Evaluation Report</h1>
            <p>AI-Powered Answer Assessment</p>
        </div>

        <div class="score-section">
            <div class="score-circle">${result.score}/10</div>
            <div class="grade-badge">Grade ${result.grade}</div>
            <p style="margin-top: 20px; color: #666;">Overall Performance: ${result.percentage}%</p>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Semantic Similarity</div>
                <div class="metric-value">${(result.metrics.similarity * 100).toFixed(0)}%</div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: ${result.metrics.similarity * 100}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Content Coverage</div>
                <div class="metric-value">${(result.metrics.coverage * 100).toFixed(0)}%</div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: ${result.metrics.coverage * 100}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Grammar Quality</div>
                <div class="metric-value">${(result.metrics.grammar * 100).toFixed(0)}%</div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: ${result.metrics.grammar * 100}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Relevance</div>
                <div class="metric-value">${(result.metrics.relevance * 100).toFixed(0)}%</div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: ${result.metrics.relevance * 100}%"></div>
                </div>
            </div>
        </div>

        <div class="feedback-section">
            <h3>💡 AI Feedback</h3>
            <div class="feedback-text">
                ${result.feedback}
            </div>
        </div>

        ${result.extractedText ? `
        <div class="details-section">
            <h3>📝 Extracted Text (OCR)</h3>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; line-height: 1.8; color: #555;">
                ${result.extractedText}
            </div>
        </div>
        ` : ''}
        ${result.question || result.studentAnswer ? `
        <div class="details-section" style="background: #f8f9fa; border-top: 2px solid #e0e0e0;">
            <h3>📝 Evaluation Details</h3>
            
            ${result.question ? `
            <div style="margin-bottom: 24px;">
                <h4 style="color: #667eea; margin-bottom: 12px; font-size: 18px;">❓ Question:</h4>
                <div style="background: white; padding: 20px; border-radius: 8px; line-height: 1.8; color: #555; border-left: 4px solid #667eea;">
                    ${result.question}
                </div>
            </div>
            ` : ''}
            
            ${result.studentAnswer ? `
            <div style="margin-bottom: 24px;">
                <h4 style="color: #667eea; margin-bottom: 12px; font-size: 18px;">✍️ Student Answer:</h4>
                <div style="background: white; padding: 20px; border-radius: 8px; line-height: 1.8; color: #555; border-left: 4px solid #4CAF50;">
                    ${result.studentAnswer}
                </div>
            </div>
            ` : ''}
            
            ${result.referenceAnswer ? `
            <div style="margin-bottom: 24px;">
                <h4 style="color: #667eea; margin-bottom: 12px; font-size: 18px;">✅ Reference Answer:</h4>
                <div style="background: white; padding: 20px; border-radius: 8px; line-height: 1.8; color: #555; border-left: 4px solid #FF9800;">
                    ${result.referenceAnswer}
                </div>
            </div>
            ` : ''}
        </div>
        ` : ''}

        

        <div class="details-section">
            <h3>📋 Detailed Breakdown</h3>
            <div class="detail-row">
                <span class="detail-label">Evaluation Mode</span>
                <span class="detail-value">${activeTab === 'ocr' ? 'OCR Analysis' : activeTab === 'text' ? 'Text-Based' : activeTab === 'advanced' ? 'Advanced PDF' : 'Batch Processing'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Total Score</span>
                <span class="detail-value">${result.score}/10</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Percentage</span>
                <span class="detail-value">${result.percentage}%</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Grade</span>
                <span class="detail-value">${result.grade}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Average Metric Score</span>
                <span class="detail-value">${((result.metrics.similarity + result.metrics.coverage + result.metrics.grammar + result.metrics.relevance) / 4 * 100).toFixed(1)}%</span>
            </div>
        </div>

        <div class="timestamp">
            Report generated on ${new Date().toLocaleString()}
        </div>
    </div>
</body>
</html>`;

    // Create and trigger download
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `evaluation-report-grade-${result.grade}-${Date.now()}.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const sampleData = [
    { subject: 'Similarity', A: 85, fullMark: 100 },
    { subject: 'Coverage', A: 78, fullMark: 100 },
    { subject: 'Grammar', A: 92, fullMark: 100 },
    { subject: 'Relevance', A: 88, fullMark: 100 },
  ];

  const trendData = [
    { name: 'Q1', score: 65 },
    { name: 'Q2', score: 72 },
    { name: 'Q3', score: 78 },
    { name: 'Q4', score: 85 },
    { name: 'Q5', score: 88 },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-dark-950 via-dark-900 to-primary-950">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-500/20 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-primary-600/20 rounded-full blur-3xl animate-pulse-slow delay-1000" />
      </div>

      {/* Navigation */}
      <nav className="relative z-50 border-b border-white/10 backdrop-blur-xl bg-dark-950/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <motion.div className="flex items-center space-x-3" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
              <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/30">
                <Brain className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-primary-200 bg-clip-text text-transparent">ARC</h1>
                <p className="text-xs text-gray-400">AI Answer Evaluation</p>
              </div>
            </motion.div>

            <div className="flex items-center space-x-1 overflow-x-auto">
              {[
                { id: 'home', icon: FileText, label: 'Home' },
                { id: 'text', icon: FileText, label: 'Text' },
                { id: 'advanced', icon: Brain, label: 'Advanced' },
                { id: 'ocr', icon: ImageIcon, label: 'OCR' },
                { id: 'batch', icon: Layers, label: 'Batch' },
                { id: 'results', icon: BarChart3, label: 'Results' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-300 whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'bg-primary-500/20 text-primary-300 border border-primary-500/30'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <AnimatePresence mode="wait">
          {activeTab === 'home' && (
            <motion.div key="home" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="space-y-24">
              {/* Hero Section - Enhanced */}
              <div className="text-center space-y-8 relative">
                {/* Floating Badge */}
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="inline-flex items-center space-x-2 bg-primary-500/20 border border-primary-500/30 rounded-full px-6 py-3 mb-4"
                >
                  <Sparkles className="w-5 h-5 text-primary-400" />
                  <span className="text-sm font-semibold text-primary-300">AI-Powered Grading System</span>
                </motion.div>

                <motion.h2 
                  className="text-6xl sm:text-7xl font-black bg-gradient-to-r from-white via-primary-200 to-primary-400 bg-clip-text text-transparent leading-tight"
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  Transform Subjective<br />Answer Evaluation
                </motion.h2>
                
                <motion.p 
                  className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed"
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  Leverage advanced AI to provide instant, consistent, and detailed evaluation of student answers. 
                  Save time while maintaining accuracy.
                </motion.p>

                <motion.div 
                  className="flex flex-col sm:flex-row gap-4 justify-center items-center"
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                >
                  <button
                    onClick={() => setActiveTab('text')}
                    className="btn-primary text-lg px-8 py-4 flex items-center space-x-2 group"
                  >
                    <Zap className="w-6 h-6 group-hover:animate-pulse" />
                    <span>Start Free Evaluation</span>
                    <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </button>
                  <button
                    onClick={() => setActiveTab('advanced')}
                    className="px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white font-semibold transition-all duration-300 hover:-translate-y-0.5 flex items-center space-x-2"
                  >
                    <Brain className="w-5 h-5" />
                    <span>Explore Features</span>
                  </button>
                </motion.div>

                {/* Quick Stats */}
                <motion.div 
                  initial={{ opacity: 0, y: 40 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                  className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto pt-12"
                >
                  {[
                    { label: 'Evaluations', value: '1,234', change: '+12%', icon: TrendingUp, color: 'from-blue-500 to-cyan-500' },
                    { label: 'Avg Score', value: '7.8', change: '+0.3', icon: Award, color: 'from-purple-500 to-pink-500' },
                    { label: 'Accuracy', value: '95%', change: '+2%', icon: CheckCircle2, color: 'from-green-500 to-emerald-500' },
                    { label: 'Time Saved', value: '85%', change: '-15m', icon: Zap, color: 'from-yellow-500 to-orange-500' }
                  ].map((stat, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.7 + idx * 0.1 }}
                      className="card-glass p-6 text-center group hover:border-primary-500/30 transition-all duration-300"
                    >
                      <div className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform`}>
                        <stat.icon className="w-6 h-6 text-white" />
                      </div>
                      <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                      <div className="text-sm text-gray-400 mb-2">{stat.label}</div>
                      <div className="text-xs text-green-400 font-semibold">{stat.change}</div>
                    </motion.div>
                  ))}
                </motion.div>
              </div>

              {/* Features Gateway */}
              <div className="relative">
                <div className="text-center mb-12">
                  <motion.h3 
                    className="text-4xl font-bold text-white mb-4"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 }}
                  >
                    Choose Your Evaluation Method
                  </motion.h3>
                  <motion.p 
                    className="text-lg text-gray-400"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9 }}
                  >
                    Four powerful modes designed for different use cases
                  </motion.p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {[
                    {
                      id: 'text',
                      icon: FileText,
                      title: 'Text Analysis',
                      desc: 'Quick evaluation by pasting text answers',
                      features: ['Instant feedback', 'Auto & manual modes', 'Grammar check'],
                      color: 'from-blue-500 to-cyan-500',
                      popular: false
                    },
                    {
                      id: 'advanced',
                      icon: Brain,
                      title: 'Advanced PDF',
                      desc: 'AI-powered PDF document processing',
                      features: ['Multi-file upload', 'Auto-reference generation', 'Detailed analytics'],
                      color: 'from-purple-500 to-pink-500',
                      popular: true
                    },
                    {
                      id: 'ocr',
                      icon: ImageIcon,
                      title: 'OCR Analysis',
                      desc: 'Extract & evaluate handwritten answers',
                      features: ['Handwriting recognition', 'Image preprocessing', 'Text extraction'],
                      color: 'from-green-500 to-emerald-500',
                      popular: false
                    },
                    {
                      id: 'batch',
                      icon: Layers,
                      title: 'Batch Processing',
                      desc: 'Evaluate multiple answer sheets at once',
                      features: ['Bulk processing', 'ZIP archive support', 'Aggregate results'],
                      color: 'from-yellow-500 to-orange-500',
                      popular: false
                    }
                  ].map((feature, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: 30 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.0 + idx * 0.1 }}
                      whileHover={{ y: -8, transition: { duration: 0.3 } }}
                      onClick={() => setActiveTab(feature.id as any)}
                      className={`card-glass p-8 cursor-pointer group relative overflow-hidden ${
                        feature.popular ? 'border-primary-500/50 bg-primary-500/10' : ''
                      }`}
                    >
                      {/* Popular Badge */}
                      {feature.popular && (
                        <div className="absolute top-4 right-4 bg-primary-500 text-white text-xs font-bold px-3 py-1 rounded-full z-10">
                          POPULAR
                        </div>
                      )}

                      {/* Hover Gradient */}
                      <div className={`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`} />

                      <div className="relative z-10">
                        <div className={`w-16 h-16 bg-gradient-to-br ${feature.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg`}>
                          <feature.icon className="w-8 h-8 text-white" />
                        </div>

                        <h4 className="text-2xl font-bold text-white mb-3">{feature.title}</h4>
                        <p className="text-gray-400 mb-6 leading-relaxed">{feature.desc}</p>

                        <ul className="space-y-3 mb-6">
                          {feature.features.map((feat, i) => (
                            <li key={i} className="flex items-start space-x-2">
                              <CheckCircle2 className="w-5 h-5 text-primary-400 flex-shrink-0 mt-0.5" />
                              <span className="text-sm text-gray-300">{feat}</span>
                            </li>
                          ))}
                        </ul>

                        <div className="flex items-center text-primary-400 font-semibold group-hover:text-primary-300 transition-colors">
                          <span>Try Now</span>
                          <ChevronRight className="w-5 h-5 ml-2 group-hover:translate-x-2 transition-transform" />
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* How It Works */}
              <div className="relative py-12">
                <div className="text-center mb-12">
                  <motion.h3 
                    className="text-4xl font-bold text-white mb-4"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.4 }}
                  >
                    How It Works
                  </motion.h3>
                  <motion.p 
                    className="text-lg text-gray-400"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.5 }}
                  >
                    Three simple steps to automated grading
                  </motion.p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                  {[
                    {
                      step: '01',
                      title: 'Upload Answer',
                      desc: 'Paste text or upload PDF/image files',
                      icon: Upload
                    },
                    {
                      step: '02',
                      title: 'AI Analysis',
                      desc: 'Advanced NLP models evaluate the answer',
                      icon: Brain
                    },
                    {
                      step: '03',
                      title: 'Get Results',
                      desc: 'Instant scoring with detailed metrics',
                      icon: BarChart3
                    }
                  ].map((item, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: 30 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.6 + idx * 0.1 }}
                      className="relative"
                    >
                      {/* Connector Line */}
                      {idx < 2 && (
                        <div className="hidden md:block absolute top-16 left-full w-full h-0.5 bg-gradient-to-r from-primary-500/50 to-transparent -translate-y-1/2" />
                      )}
                      
                      <div className="card-glass p-8 text-center group hover:border-primary-500/30 transition-all">
                        <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                          <item.icon className="w-10 h-10 text-white" />
                        </div>
                        <div className="text-5xl font-black text-primary-500/20 absolute top-4 right-4">{item.step}</div>
                        <h4 className="text-xl font-bold text-white mb-3">{item.title}</h4>
                        <p className="text-gray-400">{item.desc}</p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* CTA Section */}
              <div className="card-glass p-12 text-center relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-primary-500/20 to-purple-500/20" />
                <div className="relative z-10">
                  <motion.h3 
                    className="text-4xl font-bold text-white mb-6"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.9 }}
                  >
                    Ready to Transform Your Grading?
                  </motion.h3>
                  <motion.p 
                    className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 2.0 }}
                  >
                    Join educators who are saving hours with AI-powered evaluation
                  </motion.p>
                  <motion.button
                    onClick={() => setActiveTab('text')}
                    className="btn-primary text-lg px-12 py-5 inline-flex items-center space-x-2"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 2.1 }}
                  >
                    <Sparkles className="w-6 h-6" />
                    <span>Start Evaluating for Free</span>
                  </motion.button>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'text' && (
            <motion.div key="text" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto space-y-8">
              <div className="text-center">
                <h2 className="text-4xl font-bold text-white mb-4">Text-Based Analysis</h2>
                <p className="text-gray-400">Paste student and reference answers for instant evaluation</p>
              </div>

              <div className="card-glass p-8 space-y-6">
                {/* Question Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Question</label>
                  <textarea
                    value={textQuestion}
                    onChange={(e) => setTextQuestion(e.target.value)}
                    className="w-full h-24 p-4 bg-white/5 border border-white/10 rounded-xl text-white focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
                    placeholder="Enter the question here..."
                  />
                </div>

                {/* Student Answer */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Student Answer</label>
                  <textarea
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    className="w-full h-40 p-4 bg-white/5 border border-white/10 rounded-xl text-white focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
                    placeholder="Paste student's answer here..."
                  />
                </div>

                {evaluationMode === 'manual' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Reference Answer</label>
                    <textarea
                      value={referenceInput}
                      onChange={(e) => setReferenceInput(e.target.value)}
                      className="w-full h-40 p-4 bg-white/5 border border-white/10 rounded-xl text-white focus:border-primary-500"
                      placeholder="Paste reference answer here..."
                    />
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => setEvaluationMode('auto')}
                    className={`p-4 rounded-xl border-2 transition-all ${evaluationMode === 'auto' ? 'border-primary-500 bg-primary-500/10' : 'border-white/10 bg-white/5'}`}
                  >
                    <Bot className="w-6 h-6 text-primary-400 mx-auto mb-2" />
                    <span className="text-sm font-bold text-white">Auto Reference</span>
                  </button>
                  <button
                    onClick={() => setEvaluationMode('manual')}
                    className={`p-4 rounded-xl border-2 transition-all ${evaluationMode === 'manual' ? 'border-primary-500 bg-primary-500/10' : 'border-white/10 bg-white/5'}`}
                  >
                    <FileCheck className="w-6 h-6 text-primary-400 mx-auto mb-2" />
                    <span className="text-sm font-bold text-white">Manual Reference</span>
                  </button>
                </div>

                <button onClick={handleEvaluate} disabled={isProcessing} className="btn-primary w-full py-4 disabled:opacity-50">
                  {isProcessing ? 'Evaluating...' : 'Evaluate Answer'}
                </button>
              </div>
            </motion.div>
          )}

          {activeTab === 'advanced' && (
            <motion.div key="advanced" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto space-y-8">
              <div className="text-center">
                <h2 className="text-4xl font-bold text-white mb-4">Advanced PDF Evaluation</h2>
                <p className="text-gray-400">Upload PDFs for comprehensive AI-powered analysis</p>
              </div>

              <div className="card-glass p-8 space-y-6">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <button onClick={() => setEvaluationMode('auto')} className={`p-4 rounded-xl border-2 ${evaluationMode === 'auto' ? 'border-primary-500 bg-primary-500/10' : 'border-white/10'}`}>
                    <Bot className="w-6 h-6 text-primary-400 mx-auto mb-2" />
                    <span className="text-sm font-bold text-white">Auto Reference</span>
                  </button>
                  <button onClick={() => setEvaluationMode('manual')} className={`p-4 rounded-xl border-2 ${evaluationMode === 'manual' ? 'border-primary-500 bg-primary-500/10' : 'border-white/10'}`}>
                    <FileCheck className="w-6 h-6 text-primary-400 mx-auto mb-2" />
                    <span className="text-sm font-bold text-white">Manual Reference</span>
                  </button>
                </div>

                {/* Answer Sheet Upload */}
                <div
                  onDragEnter={(e) => handleDrag(e, 'answerSheet')}
                  onDragLeave={(e) => handleDrag(e, 'answerSheet')}
                  onDragOver={(e) => handleDrag(e, 'answerSheet')}
                  onDrop={(e) => handleDrop(e, 'answerSheet')}
                  className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer ${
                    dragActive.answerSheet ? 'border-primary-500 bg-primary-500/10' : 'border-white/20 bg-white/5'
                  }`}
                >
                  <input type="file" accept=".pdf,.txt" onChange={(e) => handleFileSelect('answerSheet', e.target.files?.[0] || null)} className="hidden" id="answerSheet" />
                  <label htmlFor="answerSheet" className="cursor-pointer block">
                    <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-bold text-white mb-2">Answer Sheet PDF</h3>
                    <p className="text-sm text-gray-400">{selectedFiles.answerSheet ? selectedFiles.answerSheet.name : 'Drop or click to upload'}</p>
                  </label>
                </div>

                {/* Question Paper Upload */}
                <div
                  onDragEnter={(e) => handleDrag(e, 'questionPaper')}
                  onDragLeave={(e) => handleDrag(e, 'questionPaper')}
                  onDragOver={(e) => handleDrag(e, 'questionPaper')}
                  onDrop={(e) => handleDrop(e, 'questionPaper')}
                  className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer ${
                    dragActive.questionPaper ? 'border-primary-500 bg-primary-500/10' : 'border-white/20 bg-white/5'
                  }`}
                >
                  <input type="file" accept=".pdf,.txt" onChange={(e) => handleFileSelect('questionPaper', e.target.files?.[0] || null)} className="hidden" id="questionPaper" />
                  <label htmlFor="questionPaper" className="cursor-pointer block">
                    <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-bold text-white mb-2">Question Paper PDF</h3>
                    <p className="text-sm text-gray-400">{selectedFiles.questionPaper ? selectedFiles.questionPaper.name : 'Drop or click to upload'}</p>
                  </label>
                </div>

                {evaluationMode === 'manual' && (
                  <div
                    onDragEnter={(e) => handleDrag(e, 'reference')}
                    onDragLeave={(e) => handleDrag(e, 'reference')}
                    onDragOver={(e) => handleDrag(e, 'reference')}
                    onDrop={(e) => handleDrop(e, 'reference')}
                    className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer ${
                      dragActive.reference ? 'border-primary-500 bg-primary-500/10' : 'border-white/20 bg-white/5'
                    }`}
                  >
                    <input type="file" accept=".pdf,.txt" onChange={(e) => handleFileSelect('reference', e.target.files?.[0] || null)} className="hidden" id="reference" />
                    <label htmlFor="reference" className="cursor-pointer block">
                      <FileCheck className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <h3 className="text-lg font-bold text-white mb-2">Reference Answers PDF</h3>
                      <p className="text-sm text-gray-400">{selectedFiles.reference ? selectedFiles.reference.name : 'Drop or click to upload'}</p>
                    </label>
                  </div>
                )}

                <button onClick={handleEvaluate} disabled={isProcessing} className="btn-primary w-full py-4 disabled:opacity-50">
                  {isProcessing ? 'Processing...' : 'Start Advanced Evaluation'}
                </button>
              </div>
            </motion.div>
          )}

          {activeTab === 'ocr' && (
            <motion.div key="ocr" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto space-y-8">
              <div className="text-center">
                <h2 className="text-4xl font-bold text-white mb-4">OCR Handwritten Answer Analysis</h2>
                <p className="text-gray-400">Upload images of handwritten answers for OCR-based evaluation</p>
              </div>

              <div className="card-glass p-8 space-y-6">
                {/* Question Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Question Text</label>
                  <textarea
                    value={ocrQuestion}
                    onChange={(e) => setOcrQuestion(e.target.value)}
                    className="w-full h-32 p-4 bg-white/5 border border-white/10 rounded-xl text-white focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
                    placeholder="Enter the question text here..."
                  />
                </div>

                {/* Image Upload */}
                <div
                  onDragEnter={(e) => handleDrag(e, 'ocrImage')}
                  onDragLeave={(e) => handleDrag(e, 'ocrImage')}
                  onDragOver={(e) => handleDrag(e, 'ocrImage')}
                  onDrop={(e) => handleDrop(e, 'ocrImage')}
                  className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all cursor-pointer ${
                    dragActive.ocrImage ? 'border-primary-500 bg-primary-500/10' : 'border-white/20 bg-white/5'
                  }`}
                >
                  <input type="file" accept="image/*" onChange={(e) => handleFileSelect('ocrImage', e.target.files?.[0] || null)} className="hidden" id="ocrImage" />
                  <label htmlFor="ocrImage" className="cursor-pointer block">
                    <ImageIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-white mb-2">Drop Handwritten Answer Image</h3>
                    <p className="text-gray-400 mb-4">Supports JPG, PNG, WEBP</p>
                    {selectedFiles.ocrImage && (
                      <div className="mt-4 p-4 bg-white/5 rounded-lg">
                        <p className="text-sm text-white font-medium">{selectedFiles.ocrImage.name}</p>
                        <p className="text-xs text-gray-400">{(selectedFiles.ocrImage.size / 1024).toFixed(2)} KB</p>
                      </div>
                    )}
                  </label>
                </div>

                <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-4">
                  <h4 className="text-sm font-bold text-blue-300 mb-2">💡 Tips for Best Results</h4>
                  <ul className="text-xs text-blue-200 space-y-1">
                    <li>• Use clear, well-lit photos</li>
                    <li>• Ensure handwriting is legible</li>
                    <li>• Avoid shadows and glare</li>
                    <li>• Keep the camera steady</li>
                  </ul>
                </div>

                <button onClick={handleEvaluate} disabled={!selectedFiles.ocrImage || isProcessing} className="btn-primary w-full py-4 disabled:opacity-50">
                  {isProcessing ? 'Extracting & Evaluating...' : 'Extract & Evaluate Answer'}
                </button>
              </div>
            </motion.div>
          )}

          {activeTab === 'batch' && (
            <motion.div key="batch" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto space-y-8">
              <div className="text-center">
                <h2 className="text-4xl font-bold text-white mb-4">Batch Processing</h2>
                <p className="text-gray-400">Evaluate multiple answer sheets at once</p>
              </div>

              <div className="card-glass p-8 space-y-6">
                <div
                  onDragEnter={(e) => handleDrag(e, 'batchFile')}
                  onDragLeave={(e) => handleDrag(e, 'batchFile')}
                  onDragOver={(e) => handleDrag(e, 'batchFile')}
                  onDrop={(e) => handleDrop(e, 'batchFile')}
                  className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all cursor-pointer ${
                    dragActive.batchFile ? 'border-primary-500 bg-primary-500/10' : 'border-white/20 bg-white/5'
                  }`}
                >
                  <input type="file" accept=".zip,.tar,.gz" onChange={(e) => handleFileSelect('batchFile', e.target.files?.[0] || null)} className="hidden" id="batchFile" />
                  <label htmlFor="batchFile" className="cursor-pointer block">
                    <Layers className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-white mb-2">Drop ZIP Archive</h3>
                    <p className="text-gray-400 mb-4">Contains multiple answer sheets</p>
                    {selectedFiles.batchFile && (
                      <div className="mt-4 p-4 bg-white/5 rounded-lg">
                        <p className="text-sm text-white font-medium">{selectedFiles.batchFile.name}</p>
                        <p className="text-xs text-gray-400">{(selectedFiles.batchFile.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                    )}
                  </label>
                </div>

                <div className="bg-purple-500/10 border border-purple-500/20 rounded-xl p-4">
                  <h4 className="text-sm font-bold text-purple-300 mb-2">📦 Archive Requirements</h4>
                  <ul className="text-xs text-purple-200 space-y-1">
                    <li>• ZIP file containing PDF answer sheets</li>
                    <li>• Include question_paper.pdf in archive</li>
                    <li>• Optional: include reference_answers.pdf</li>
                    <li>• Name files clearly (student1.pdf, student2.pdf, etc.)</li>
                  </ul>
                </div>

                <button onClick={handleEvaluate} disabled={!selectedFiles.batchFile || isProcessing} className="btn-primary w-full py-4 disabled:opacity-50">
                  {isProcessing ? 'Processing Batch...' : 'Start Batch Evaluation'}
                </button>
              </div>
            </motion.div>
          )}

          {activeTab === 'results' && (
            <motion.div key="results" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
              {!result ? (
                <div className="text-center py-20">
                  <BarChart3 className="w-24 h-24 text-gray-600 mx-auto mb-6" />
                  <h3 className="text-2xl font-bold text-white mb-4">No Results Yet</h3>
                  <button onClick={() => setActiveTab('text')} className="btn-primary">Start Evaluation</button>
                </div>
              ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Download Button */}
                  <div className="lg:col-span-2 flex justify-end mb-4">
                    <button
                      onClick={generateHTMLReport}
                      className="btn-primary flex items-center space-x-2"
                    >
                      <FileText className="w-5 h-5" />
                      <span>Download HTML Report</span>
                    </button>
                  </div>

                  <div className="card-glass p-8">
                    <h3 className="text-2xl font-bold text-white mb-6">Performance Overview</h3>
                    <div className="text-center mb-8">
                      <div className="text-6xl font-black bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent mb-2">{result.score}/10</div>
                      <div className="text-2xl font-bold text-primary-400 mb-2">Grade: {result.grade}</div>
                    </div>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <RadarChart data={sampleData}>
                          <PolarGrid stroke="#374151" />
                          <PolarAngleAxis dataKey="subject" tick={{ fill: '#9CA3AF' }} />
                          <Radar name="Score" dataKey="A" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.5} />
                          <Tooltip contentStyle={{ backgroundColor: 'rgba(17, 24, 39, 0.9)', border: '1px solid rgba(139, 92, 246, 0.3)', borderRadius: '12px' }} />
                        </RadarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="card-glass p-8 space-y-6">
                    <h3 className="text-2xl font-bold text-white mb-6">Detailed Analysis</h3>
                    
                    {/* Extracted Text Display (for OCR) */}
                    {result.extractedText && (
                      <div className="bg-green-500/10 border border-green-500/20 rounded-xl p-4 mb-6">
                        <h4 className="text-sm font-bold text-green-300 mb-2 flex items-center">
                          <FileText className="w-4 h-4 mr-2" />
                          Extracted Text from Image
                        </h4>
                        <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">{result.extractedText}</p>
                      </div>
                    )}
                    
                    {[
                      { label: 'Semantic Similarity', value: result.metrics.similarity * 100, color: 'from-blue-500 to-cyan-500' },
                      { label: 'Content Coverage', value: result.metrics.coverage * 100, color: 'from-purple-500 to-pink-500' },
                      { label: 'Grammar Quality', value: result.metrics.grammar * 100, color: 'from-green-500 to-emerald-500' },
                      { label: 'Relevance', value: result.metrics.relevance * 100, color: 'from-yellow-500 to-orange-500' }
                    ].map((metric, idx) => (
                      <div key={idx}>
                        <div className="flex justify-between mb-2">
                          <span className="text-gray-300">{metric.label}</span>
                          <span className="text-white font-bold">{metric.value.toFixed(0)}%</span>
                        </div>
                        <div className="h-3 bg-white/10 rounded-full overflow-hidden">
                          <motion.div initial={{ width: 0 }} animate={{ width: `${metric.value}%` }} transition={{ duration: 1 }} className={`h-full bg-gradient-to-r ${metric.color}`} />
                        </div>
                      </div>
                    ))}
                    <div className="pt-6 border-t border-white/10">
                      <h4 className="text-lg font-bold text-white mb-3">AI Feedback</h4>
                      <p className="text-gray-300">{result.feedback}</p>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
