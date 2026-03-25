# CNN Integration Guide

## Overview

The Answer Evaluation System now includes **CNN (Convolutional Neural Network)** integration for advanced semantic scoring. The CNN model works alongside Sentence Transformers to provide more accurate and nuanced evaluation of student answers.

## Architecture

### Models Used

1. **Sentence Transformers** (Default)
   - `all-MiniLM-L6-v2` - Fast, lightweight
   - `all-mpnet-base-v2` - More accurate, slower
   
2. **CNN Model** (Optional)
   - File: `cnn_answer_evaluator.h5`
   - Type: Deep learning model for semantic similarity
   - Requires: `tokenizer.pkl` for text preprocessing

3. **Hybrid Approach** (Recommended)
   - Combines CNN + Sentence Transformers
   - Configurable weights for each component
   - Default: 40% CNN, 60% Transformer

## Features Added

### 1. CNN Scoring Methods

Located in `models.py`:

- **`compute_cnn_score(reference, student)`**
  - Scores similarity using CNN only
  - Returns: Score between 0-1
  
- **`compute_hybrid_score(reference, student, question, cnn_weight, transformer_weight)`**
  - Combines CNN and Sentence Transformer scores
  - Configurable weights
  - Returns: Combined score between 0-1

### 2. Updated API Endpoint

**POST `/evaluate`**

Query Parameters:
- `use_cnn=true|false` (optional) - Enable CNN scoring
- Default: `false` (uses only Sentence Transformers)

Example Request:
```bash
curl -X POST "http://127.0.0.1:8000/evaluate?use_cnn=true" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain photosynthesis",
    "reference_answer": "...",
    "student_answer": "..."
  }'
```

Example Response (with CNN):
```json
{
  "final_score": 8.5,
  "grade": "A",
  "similarity": 0.85,
  "coverage": 0.78,
  "grammar": 0.92,
  "relevance": 0.88,
  "cnn_score": 0.82,  // Included when use_cnn=true
  "feedback": "Excellent answer!"
}
```

### 3. Configuration Options

Add to `.env` file:

```bash
# CNN Settings
USE_CNN_BY_DEFAULT=false
CNN_WEIGHT=0.30  # Weight for CNN in hybrid scoring (0-1)

# Adjust other weights if needed (must sum to 1.0 with CNN weight)
WEIGHT_SIMILARITY=0.28  # Reduced from 0.40
WEIGHT_COVERAGE=0.175   # Reduced from 0.25
WEIGHT_GRAMMAR=0.105    # Reduced from 0.15
WEIGHT_RELEVANCE=0.14   # Reduced from 0.20
```

**Note**: When using CNN, all other weights are automatically scaled down proportionally to accommodate the CNN weight.

## Usage Examples

### Python Client

```python
import requests

# Test data
data = {
    "question": "What is photosynthesis?",
    "reference_answer": "Photosynthesis is the process by which plants...",
    "student_answer": "Plants make food using sunlight..."
}

# Without CNN
response = requests.post("http://127.0.0.1:8000/evaluate", json=data)
print(response.json())

# With CNN
response = requests.post("http://127.0.0.1:8000/evaluate?use_cnn=true", json=data)
print(response.json())
```

### React Frontend

```javascript
// In your React component
const evaluateAnswer = async (answerData, useCnn = false) => {
  const url = `http://127.0.0.1:8000/evaluate${useCnn ? '?use_cnn=true' : ''}`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(answerData)
  });
  
  const result = await response.json();
  
  if (useCnn && result.cnn_score) {
    console.log(`CNN Score: ${result.cnn_score}`);
  }
  
  return result;
};
```

## Testing

### Test Script

Run the included test script:

```bash
python test_cnn_integration.py
```

This will:
1. Test evaluation without CNN
2. Test evaluation with CNN enabled
3. Check model health status

### Manual Testing

1. **Start Backend**:
   ```bash
   python app.py
   ```

2. **Check Health**:
   ```bash
   curl http://127.0.0.1:8000/health
   ```
   
   Expected output:
   ```json
   {
     "status": "healthy",
     "models": {
       "cnn_model_loaded": true,
       "tokenizer_loaded": true,
       "sentence_transformers_loaded": 2
     }
   }
   ```

3. **Test Evaluation**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/evaluate?use_cnn=true" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Test question",
       "reference_answer": "Reference answer",
       "student_answer": "Student answer"
     }'
   ```

## Performance Considerations

### Speed
- **Without CNN**: ~50-100ms per evaluation
- **With CNN**: ~150-300ms per evaluation
- CNN adds latency but improves accuracy

### Accuracy
Based on typical results:
- **Sentence Transformers only**: Good semantic understanding
- **CNN only**: Excellent pattern matching
- **Hybrid (recommended)**: Best of both approaches

### Resource Usage
- CNN model loads into memory (~50-100MB)
- GPU acceleration available if TensorFlow-GPU installed
- Falls back to CPU if no GPU available

## Troubleshooting

### CNN Model Not Loading

**Symptom**: `cnn_model_loaded: false` in health check

**Solutions**:
1. Verify file exists: `cnn_answer_evaluator.h5`
2. Check file permissions
3. Ensure TensorFlow is installed: `pip install tensorflow`
4. Check backend logs for errors

### Tokenizer Not Found

**Symptom**: `tokenizer_loaded: false`

**Solutions**:
1. Verify file exists: `tokenizer.pkl`
2. Check file path in config
3. Ensure pickle module can read the file

### CNN Scoring Returns 0

**Possible Causes**:
1. Model not loaded properly
2. Tokenizer mismatch
3. Input text too short/long
4. Model architecture mismatch

**Debug Steps**:
```python
from models import get_model_manager

mm = get_model_manager()
print(f"CNN Available: {mm.cnn_model is not None}")
print(f"Tokenizer Available: {mm.tokenizer is not None}")

# Test CNN scoring directly
score = mm.compute_cnn_score("reference", "student")
print(f"CNN Score: {score}")
```

## Advanced Configuration

### Custom CNN Weight

```python
from scoring import ScoreCalculator

# Use custom CNN weight
calculator = ScoreCalculator(use_cnn=True, cnn_weight=0.5)
```

### Hybrid Score with Question Relevance

```python
from models import get_model_manager

mm = get_model_manager()

# Get hybrid score including question relevance
hybrid_score = mm.compute_hybrid_score(
    reference="Reference answer",
    student="Student answer",
    question="Question text",
    cnn_weight=0.4,
    transformer_weight=0.6
)
```

## Migration Notes

### Existing Evaluations
- Existing evaluations continue to work without changes
- CNN is opt-in via query parameter
- No breaking changes to API

### Database Schema
- No database schema changes required
- CNN scores are NOT stored in database (can be added if needed)

### Frontend Compatibility
- Frontend continues to work without modifications
- CNN scoring is transparent to UI
- Can add UI toggle for CNN if desired

## Future Enhancements

Potential improvements:
- [ ] Store CNN scores in database for analytics
- [ ] Add CNN confidence metrics
- [ ] Implement attention visualization
- [ ] Support multiple CNN models
- [ ] Add CNN-specific feedback generation
- [ ] Batch processing optimization

## Summary

✅ **CNN is now functional and integrated**
- Loaded automatically on startup
- Available via `use_cnn=true` query parameter
- Configurable weight via `CNN_WEIGHT` setting
- Works alongside existing scoring methods
- No breaking changes

🎯 **Recommended Usage**
- Use hybrid approach (CNN + Transformers)
- Set CNN weight between 0.3-0.5
- Monitor performance impact
- Test with your specific use case

📊 **Performance**
- Slight latency increase (~100-200ms)
- Improved scoring accuracy
- Better pattern recognition
- More nuanced evaluations
