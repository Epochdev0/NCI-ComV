# Exoplanet Classification FastAPI Server

A FastAPI-based machine learning API for classifying exoplanet candidates using NASA Kepler data. Compatible with the [Exo-Vision Explorer](https://github.com/Epochdev0/exo-vision-explorer) frontend.

## Features

- **Single Prediction**: Classify individual exoplanet candidates
- **Batch Prediction**: Process multiple candidates at once
- **File Upload**: Upload CSV files for batch processing
- **Model Management**: Health checks, model info, and reload capabilities
- **Interactive Documentation**: Built-in Swagger UI at `/docs`
- **CORS Support**: Ready for web applications

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model

First, train a model using the NASA exoplanet data:

```bash
cd src
python prepare_model.py
```

This will:
- Load and clean the NASA exoplanet data
- Create binary labels (CONFIRMED = 1, others = 0)
- Train a RandomForest classifier
- Save the model to `models/baseline.pkl`

### 3. Start the Server

```bash
cd src
python api.py
```

The server will start at `http://localhost:8000`

### 4. Access the API

- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Model Info**: http://localhost:8000/model/info

## API Endpoints

### Health & Info

- `GET /` - Root endpoint with basic info
- `GET /health` - Health check
- `GET /model/info` - Model information
- `POST /model/reload` - Reload the model

### Predictions

- `POST /predict` - Simple prediction (Exo-Vision Explorer compatible)
- `POST /predict/extended` - Extended prediction with all features
- `POST /predict/batch` - Batch predictions
- `POST /predict/file` - Predict from uploaded CSV file

## Usage Examples

### Simple Prediction (Exo-Vision Explorer Compatible)

```python
import requests

# Simple features for Exo-Vision Explorer UI
features = {
    "koi_period": 15.5,
    "koi_depth": 0.005,
    "koi_duration": 3.2,
    "koi_steff": 5800
}

response = requests.post("http://localhost:8000/predict", json=features)
result = response.json()

print(f"Prediction: {result['prediction']}")  # 0 or 1
print(f"Probability: {result['probability']:.3f}")
```

### Extended Prediction

```python
import requests

# Extended features with all available data
features = {
    "kepid": 10797460,
    "koi_period": 9.48803557,
    "koi_depth": 615.8,
    "koi_duration": 2.9575,
    "koi_impact": 0.146,
    "koi_model_snr": 35.8,
    "koi_steff": 5455,
    "koi_slogg": 4.467,
    "koi_srad": 0.927,
    "koi_kepmag": 15.347,
    "ra": 291.93423,
    "dec": 48.141651
}

response = requests.post("http://localhost:8000/predict/extended", json=features)
result = response.json()

print(f"Prediction: {result['prediction']}")  # 0 or 1
print(f"Probability: {result['probability']:.3f}")
print(f"Kepler ID: {result.get('kepid', 'N/A')}")
```

### Batch Prediction

```python
import requests

# Multiple exoplanet candidates
features_list = [
    {
        "koi_period": 9.48803557,
        "koi_depth": 615.8,
        "koi_prad": 2.26,
        # ... other features
    },
    {
        "koi_period": 12.34567890,
        "koi_depth": 800.5,
        "koi_prad": 1.85,
        # ... other features
    }
]

response = requests.post("http://localhost:8000/predict/batch", json=features_list)
result = response.json()

for i, pred in enumerate(result['predictions']):
    print(f"Candidate {i+1}: {pred['prediction']} (prob: {pred['probability']:.3f})")
```

### File Upload

```python
import requests

# Upload a CSV file with exoplanet data
with open('exoplanet_data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post("http://localhost:8000/predict/file", files=files)

result = response.json()
print(f"Processed {result['total_samples']} candidates")
```

### Using curl

```bash
# Single prediction
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "koi_period": 9.48803557,
       "koi_depth": 615.8,
       "koi_prad": 2.26,
       "koi_teq": 793.0
     }'

# Health check
curl "http://localhost:8000/health"

# Model info
curl "http://localhost:8000/model/info"
```

## Data Format

The API expects exoplanet features in the following format:

```json
{
  "koi_period": 9.48803557,
  "koi_depth": 615.8,
  "koi_duration": 2.9575,
  "koi_impact": 0.146,
  "koi_model_snr": 35.8,
  "koi_steff": 5455,
  "koi_slogg": 4.467,
  "koi_srad": 0.927,
  "koi_kepmag": 15.347,
  "ra": 291.93423,
  "dec": 48.141651
}
```

## Response Format

```json
{
  "prediction": 1,
  "probability": 0.85,
  "kepid": 10797460
}
```

- `prediction`: 0 (false positive) or 1 (confirmed planet)
- `probability`: Confidence score (0.0 to 1.0)
- `kepid`: Kepler ID if provided

## Exo-Vision Explorer Integration

This API is designed to work with the [Exo-Vision Explorer](https://github.com/Epochdev0/exo-vision-explorer) frontend. To integrate:

### 1. Update Frontend API Calls

Replace the Supabase function calls in the frontend with direct API calls to your FastAPI server:

```typescript
// In src/pages/Index.tsx, replace the Supabase call:
const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    koi_period: koiPeriod,
    koi_depth: koiDepth,
    koi_duration: koiDuration,
    koi_steff: koiSteff,
  }),
});

const data = await response.json();
```

### 2. CORS Configuration

The API already includes CORS middleware to allow cross-origin requests from the frontend.

### 3. Testing Integration

Use the provided test script to verify compatibility:

```bash
python test_exo_vision_api.py
```

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Set model path and other configs
2. **Security**: Configure CORS origins appropriately
3. **Monitoring**: Add logging and metrics
4. **Scaling**: Use Gunicorn with multiple workers
5. **Model Versioning**: Implement model versioning system

### Using Gunicorn

```bash
pip install gunicorn
gunicorn src.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python src/prepare_model.py

EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest tests/
```

### Adding New Features

1. Update the `ExoplanetFeatures` model for new input fields
2. Modify the `preprocess_features` function
3. Add new endpoints as needed
4. Update documentation

## Troubleshooting

### Model Not Loading

- Check if `models/baseline.pkl` exists
- Verify the model was trained successfully
- Check file permissions

### Prediction Errors

- Ensure all required features are provided
- Check feature data types and ranges
- Verify the model is loaded (`GET /health`)

### Performance Issues

- Use batch predictions for multiple samples
- Consider model optimization
- Monitor server resources
