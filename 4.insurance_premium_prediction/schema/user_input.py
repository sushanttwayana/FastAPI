from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal
from config.city_tier import tier_1_cities, tier_2_cities


## pydantic model to validate incoming data
class UserInput(BaseModel):
    
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the person in years")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the person in kilograms")]
    height: Annotated[float, Field(..., gt=0, description="Height of the person in meters")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual salary of the user in lpa")]
    smoker: Annotated[Literal['yes', 'no'], Field(..., description="Whether the person is a smoker")]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job', 'it'], Field(..., description="Occupation of the person")]
    
    ## foe normalizing the city name
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        
        v = v.strip().title()
        return v

    
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