from fastapi import  FastAPI, HTTPException
import pickle
import json
import pandas as pd
from schema.user_input import UserInput
from fastapi.responses import JSONResponse
from ml_model_training.predict import predict_output, MODEL_VERSION, model
from schema.prediction_response import PredictionResponse
 
app = FastAPI()
        
#human readable home endpoint        
@app.get("/")
def home():
    return {"message": "Welcome to Insurance Premium Prediction API"}        

## machine readable health check endpoint      
@app.get('/health')
def health_check():
    return {
        "status": "API is healthy and running",
        'version': MODEL_VERSION,
        'model_loaded': model is not None,
        }        
        
@app.post('/patient/predict_insurance_premium', response_model=PredictionResponse)
def predict_insurance_premium(user_input: UserInput):
    
    user_input = {
        'bmi': user_input.bmi, 
        'age_group': user_input.age_group,
        'lifestyle_risk': user_input.lifestyle_risk,
        'city_tier': user_input.city_tier,
        'occupation': user_input.occupation,
        'income_lpa': user_input.income_lpa    
    }
    
    try: 
        prediction = predict_output(user_input)
        
        # return JSONResponse(status_code=200, content={'predicted_category': prediction})
        
        return JSONResponse(
        status_code=200,
        content={
            "response": {
                "predicted_category": prediction
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
