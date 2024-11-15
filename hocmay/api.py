from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import joblib
import pandas as pd
from tensorflow.keras.models import load_model

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên specify domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model và scaler
try:
    model = load_model('stock_model.h5')
    scaler = joblib.load('scaler.save')
except Exception as e:
    print(f"Error loading model: {e}")

class StockInput(BaseModel):
    values: Dict[str, float]

def predict_from_custom_input(input_values, model, scaler):
    try:
        # Chuyển đổi input thành DataFrame
        df = pd.DataFrame([input_values])
        
        # Kiểm tra dữ liệu đầu vào
        required_features = ['9/30/2024', '6/30/2024', '3/31/2024', '12/31/2023', '9/30/2023']
        missing_features = [f for f in required_features if f not in df.columns]
        if missing_features:
            return {
                'status': 'error',
                'message': f'Missing required features: {missing_features}',
                'prediction': None
            }
            
        # Chuẩn hóa dữ liệu
        X = df[required_features].values
        X_scaled = scaler.transform(X)
        
        # Dự đoán
        prediction = model.predict(X_scaled)[0][0]
        
        return {
            'status': 'success',
            'message': 'Prediction successful',
            'prediction': float(prediction),
            'input_values': input_values
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'prediction': None
        }

@app.get("/")
async def root():
    return {"message": "Stock Prediction API is running"}

@app.post("/predict")
async def predict(stock_input: StockInput):
    result = predict_from_custom_input(stock_input.values, model, scaler)
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
        
    return result 