def predict_from_custom_input(input_values, model, scaler):
    """
    Dự đoán dựa trên các giá trị Price/Sales được nhập vào
    
    Parameters:
    input_values (dict): Dictionary chứa các giá trị Price/Sales theo ngày
        Ví dụ: {
            '9/30/2024': 10.5,
            '6/30/2024': 9.8,
            '3/31/2024': 9.2,
            '12/31/2023': 8.9,
            '9/30/2023': 8.5
        }
    """
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