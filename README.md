# 🌌 NCI-ComV: Exoplanet Classification ML API

A machine learning API for classifying exoplanet candidates using NASA Kepler data. This project provides both a FastAPI backend for predictions and a Streamlit web interface for interactive exploration.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd NCI-ComV
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model** (if not already trained)
   ```bash
   python src/prepare_model.py
   ```

5. **Start the FastAPI server**
   ```bash
   python start_server.py
   ```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### Core Endpoints

- **`GET /`** - Root endpoint with API information
- **`GET /health`** - Health check and model status
- **`GET /model/info`** - Model information and metadata
- **`GET /docs`** - Interactive API documentation (Swagger UI)

### Prediction Endpoints

- **`POST /predict`** - Simple prediction with 4 core features
- **`POST /predict/extended`** - Extended prediction with all 11 features
- **`POST /predict/batch`** - Batch predictions (up to 1000 samples)
- **`POST /predict/file`** - Predictions from uploaded CSV file

### Model Management

- **`POST /model/reload`** - Reload the trained model

## 🎯 Usage Examples

### Simple Prediction (4 features)
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "koi_period": 365.25,
       "koi_depth": 0.001,
       "koi_duration": 12.0,
       "koi_steff": 5778.0
     }'
```

### Extended Prediction (11 features)
```bash
curl -X POST "http://localhost:8000/predict/extended" \
     -H "Content-Type: application/json" \
     -d '{
       "kepid": 12345,
       "koi_period": 365.25,
       "koi_depth": 1000.0,
       "koi_duration": 12.0,
       "koi_impact": 0.5,
       "koi_model_snr": 20.0,
       "koi_steff": 5778.0,
       "koi_slogg": 4.5,
       "koi_srad": 1.0,
       "koi_kepmag": 15.0,
       "ra": 300.0,
       "dec": 50.0
     }'
```

### Batch Prediction
```bash
curl -X POST "http://localhost:8000/predict/batch" \
     -H "Content-Type: application/json" \
     -d '[
       {
         "koi_period": 365.25,
         "koi_depth": 1000.0,
         "koi_duration": 12.0,
         "koi_steff": 5778.0
       },
       {
         "koi_period": 10.0,
         "koi_depth": 500.0,
         "koi_duration": 2.0,
         "koi_steff": 4000.0
       }
     ]'
```

## 🌐 Web Interface

### Streamlit App
Run the interactive web interface:

```bash
streamlit run webapp/streamlit_app.py
```

The Streamlit app will be available at `http://localhost:8501`

## 📊 Model Information

### Features Used
The model uses 11 features for exoplanet classification:

1. **koi_period** - Orbital Period [days]
2. **koi_depth** - Transit Depth [ppm]
3. **koi_duration** - Transit Duration [hours]
4. **koi_impact** - Impact Parameter
5. **koi_model_snr** - Signal-to-Noise Ratio
6. **koi_steff** - Stellar Effective Temperature [K]
7. **koi_slogg** - Stellar Surface Gravity [log10(cm/s²)]
8. **koi_srad** - Stellar Radius [Solar radii]
9. **koi_kepmag** - Kepler-band [mag]
10. **ra** - Right Ascension [decimal degrees]
11. **dec** - Declination [decimal degrees]

### Model Details
- **Algorithm**: XGBoost Classifier
- **Training Data**: NASA Kepler Exoplanet Archive
- **Classes**: 
  - `0` = False Positive/Candidate
  - `1` = Confirmed Planet
- **Performance**: See model training output for detailed metrics

## 📁 Project Structure

```
NCI-ComV/
├── src/
│   ├── api.py              # FastAPI server implementation
│   ├── prepare_model.py    # Model training script
│   └── train.py           # Alternative training script
├── webapp/
│   ├── streamlit_app.py   # Streamlit web interface
│   ├── index.html         # HTML interface
│   └── style.css          # CSS styles
├── models/
│   ├── baseline.pkl       # Trained model
│   └── feature_names.txt  # Feature names reference
├── data/
│   ├── nasa_exoplanet_cumulative.csv  # Training data
│   └── sample_exoplanet_data.csv     # Sample data
├── requirements.txt       # Python dependencies
├── start_server.py       # Server startup script
├── start_dev.sh          # Development environment script
└── README.md             # This file
```

## 🔧 Development

### Running Tests
```bash
# Test API endpoints
python test_api.py

# Test with sample data
python test_exo_vision_api.py
```

### Training a New Model
```bash
# Train model with default settings
python src/prepare_model.py

# Or use the alternative training script
python src/train.py --data nasa_exoplanet_cumulative.csv --output models/baseline.pkl
```

### Development Mode
For development with both backend and frontend:
```bash
# Make sure you have the frontend directory
# Then run:
bash start_dev.sh
```

## 📝 API Response Format

### Prediction Response
```json
{
  "prediction": 1,
  "probability": 0.85,
  "kepid": 12345
}
```

### Batch Prediction Response
```json
{
  "predictions": [
    {
      "prediction": 1,
      "probability": 0.85,
      "kepid": 12345
    }
  ],
  "total_samples": 1
}
```

### Model Info Response
```json
{
  "model_path": "models/baseline.pkl",
  "model_type": "XGBClassifier",
  "is_loaded": true,
  "feature_count": 11
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Model not found error**
   - Run `python src/prepare_model.py` to train the model
   - Ensure `models/baseline.pkl` exists

2. **Import errors**
   - Activate virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

3. **Port already in use**
   - Change port in `src/api.py` or kill existing process
   - Use `lsof -ti:8000 | xargs kill` to kill process on port 8000

4. **CORS errors**
   - The API is configured to allow all origins (`*`)
   - For production, update CORS settings in `src/api.py`

### Logs
Check the console output for detailed error messages and logs.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For questions or issues:
- Check the [API Documentation](http://localhost:8000/docs) when running locally
- Review the troubleshooting section above
- Open an issue on GitHub

---

**Happy exoplanet hunting! 🚀**