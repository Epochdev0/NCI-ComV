# ExoVision Explorer - Frontend Integration

This document explains how the React frontend has been integrated with the FastAPI backend for real exoplanet prediction.

## 🚀 Quick Start

### Option 1: Use the Development Script
```bash
# Make sure you're in the project root
./start_dev.sh
```

### Option 2: Manual Setup
```bash
# Terminal 1: Start FastAPI backend
source venv/bin/activate
python start_server.py

# Terminal 2: Start React frontend
cd frontend/exo-vision-explorer
npm run dev
```

## 🔧 Integration Details

### API Service (`src/services/api.ts`)
- **Purpose**: Handles all communication with the FastAPI backend
- **Features**:
  - Type-safe request/response interfaces
  - Error handling with detailed error messages
  - Health check functionality
  - Model information retrieval

### Updated Components

#### `src/pages/Index.tsx`
- **API Status Monitoring**: Real-time connection status to the ML server
- **Error Handling**: Comprehensive error messages for different failure scenarios
- **Loading States**: Visual feedback during API calls
- **Connection Validation**: Prevents predictions when API is unavailable

### Key Features

1. **Real-time API Status**
   - Green dot: Connected and model loaded
   - Yellow spinner: Connecting
   - Red warning: Connection failed

2. **Robust Error Handling**
   - Network errors
   - Model not loaded errors
   - Invalid parameter errors
   - Server errors

3. **Type Safety**
   - TypeScript interfaces for all API calls
   - Compile-time validation of request/response data

## 🌐 API Endpoints Used

- `GET /health` - Check server and model status
- `GET /model/info` - Get model information
- `POST /predict` - Make exoplanet predictions

## 📊 Data Flow

1. **User Input**: Slider values for orbital parameters
2. **Validation**: Frontend validates input ranges
3. **API Call**: Sends POST request to `/predict` endpoint
4. **Processing**: FastAPI preprocesses features and runs ML model
5. **Response**: Returns prediction (0/1) and confidence probability
6. **Display**: Frontend shows results with animations and visual feedback

## 🔄 Parameter Mapping

| Frontend Slider | API Parameter | Description |
|----------------|---------------|-------------|
| Orbital Period | `koi_period` | Days |
| Transit Depth | `koi_depth` | Ratio (converted to ppm) |
| Transit Duration | `koi_duration` | Hours |
| Star Temperature | `koi_steff` | Kelvin |

## 🎨 UI Enhancements

- **Connection Status**: Visual indicator of API health
- **Disabled States**: Button disabled when API unavailable
- **Loading Animations**: Spinner during prediction requests
- **Error Messages**: Toast notifications for different error types
- **Responsive Design**: Works on all screen sizes

## 🛠️ Environment Configuration

The frontend automatically connects to `http://localhost:8000` by default. To change this:

1. Create `.env` file in `frontend/exo-vision-explorer/`
2. Add: `VITE_API_URL=http://your-api-url:port`

## 🧪 Testing the Integration

1. Start both servers using `./start_dev.sh`
2. Open http://localhost:5173
3. Verify the green "ML server connected" indicator
4. Adjust sliders and click "Analyze Signal"
5. Check the prediction results

## 🐛 Troubleshooting

### Frontend shows "ML server unavailable"
- Ensure FastAPI server is running on port 8000
- Check that the model file exists at `models/baseline.pkl`
- Verify no firewall blocking localhost:8000

### Predictions fail with errors
- Check browser console for detailed error messages
- Verify model is loaded (check `/health` endpoint)
- Ensure all required parameters are within valid ranges

### CORS errors
- The FastAPI server includes CORS middleware
- If issues persist, check the `allow_origins` setting in `api.py`

## 📈 Performance Notes

- **First Prediction**: May take longer due to model loading
- **Subsequent Predictions**: Typically < 100ms
- **Batch Processing**: Not implemented in UI (available via API)
- **Caching**: No caching implemented (could be added for repeated requests)

## 🔮 Future Enhancements

- **Batch Upload**: CSV file upload for multiple predictions
- **Prediction History**: Save and display previous predictions
- **Model Comparison**: Switch between different trained models
- **Real-time Updates**: WebSocket connection for live parameter updates
- **Advanced Visualization**: Plot prediction confidence over parameter ranges
