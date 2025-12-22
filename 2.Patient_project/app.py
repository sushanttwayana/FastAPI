from fastapi import  FastAPI, HTTPException
import pickle
import json
import pandas as pd
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
from fastapi.responses import JSONResponse

ml_model_path = 'ml_model_training/model.pkl'

#import the ml model
with open(ml_model_path, 'rb') as f:
    model = pickle.load(f)
    
app = FastAPI()

### user city tier list
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

## pydantic model to validate incoming data
class UserInput(BaseModel):
    
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the person in years")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the person in kilograms")]
    height: Annotated[float, Field(..., gt=0, description="Height of the person in meters")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual salary of the user in lpa")]
    smoker: Annotated[Literal['yes', 'no'], Field(..., description="Whether the person is a smoker")]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job', 'it'], Field(..., description="Occupation of the person")]
    
    
    ### creating the bmi value
    @computed_field
    @property
    def bmi(self) -> float:
        
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    ### caluclate lifestyle risk
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker == 'yes' and self.bmi > 30:
            return "high"
        elif self.smoker == 'yes' or self.bmi > 25:
            return "medium"
        else:
            return "low"
    
    ## compute the age group
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 20:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    ## compute the city tier
    @computed_field
    @property
    def city_tier(self) -> str:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post('/patient/predict_insurance_premium')
def predict_insurance_premium(user_input: UserInput):
    
    input_df = pd.DataFrame([{
        'bmi': user_input.bmi, 
        'age_group': user_input.age_group,
        'lifestyle_risk': user_input.lifestyle_risk,
        'city_tier': user_input.city_tier,
        'occupation': user_input.occupation,
        'income_lpa': user_input.income_lpa    
    }])
    
    prediction = model.predict(input_df)[0]
    
    # return JSONResponse(status_code=200, content={'predicted_category': prediction})
    
    return JSONResponse(
    status_code=200,
    content={
        "response": {
            "predicted_category": prediction
        }
    })
