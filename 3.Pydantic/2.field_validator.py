from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator('email') ### field to apply validation
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['8squarei.com', 'gmail.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1] ## last part

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='after')
    # @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 80:
            return value
        else:
            raise ValueError('Age should be in between 0 and 80')
        
    # @field_validator('age',mode='before')
    # @classmethod
    # def validate_age(cls, value):
    #     if 0 < value < 100:
    #         return value
        
    #     else:
    #         raise ValueError('Age should be in between 0 and 80')


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'sushant', 'email':'sushant@8squarei.com', 'age': '24', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info) # validation -> type coercion

update_patient_data(patient1)