# from pydantic import BaseModel, EmailStr, AnyUrl, Field
# from typing import List, Dict, Optional, Annotated

# class Patient(BaseModel):

#     name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Nitish', 'Amit'])]
#     email: EmailStr
#     linkedin_url: AnyUrl
#     age: int = Field(gt=0, lt=120)
#     weight: Annotated[float, Field(gt=0, strict=True)]
#     married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
#     allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
#     contact_details: Dict[str, str]


# def update_patient_data(patient: Patient):

#     print(patient.name)
#     print(patient.age)
#     print(patient.allergies)
#     print(patient.married)
#     print('updated')

# patient_info = {'name':'Sushant', 'email':'abc@gmail.com', 'linkedin_url':'http://linkedin.com/1322', 'age': '24', 'weight': 72,'contact_details':{'phone':'2353462'}}

# patient1 = Patient(**patient_info)

# update_patient_data(patient1)   


from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, TypedDict, Dict, Optional, Annotated

class Patient(BaseModel):
    
    name: Annotated[str, Field(max_length=50, title="Name of the patient", description="Give the name of the patient in less than 50 characters", examples=['Sushant', 'Hari Bahadur'])]
    age : int = Field(gt=0, lt= 70)
    email: EmailStr
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description=" Is the patient married or not!!")]
    linkedin_url: AnyUrl
    ## default value is none
    allergies: Annotated[Optional[List[str]] , Field(default=None, max_length=5)  ]                                            #### 2 level validation all values are str inside list
    contact_details: Dict[str, str]
    
def insert_patient_data(patient: Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.linkedin_url)
    print(patient.weight)
    print('inserted')
    
def update_patient_data(patient: Patient):
    
    print(patient.name)
    print(patient.age)
    print('inserted')
    
    

# patient_info = {'name': 'sushant', 'age': 24, 'weight': 72, 'married': False, 'allergies': ['pollen', 'dust'], 'contact_details': {'email': 'abc@gmail.com', 'phone': '1234567890'} }
patient_info = {'name': 'sushant', 'email': 'abc@gmail.com', 'age': 24, 'weight': 72.02, 'contact_details': {'email': 'abc@gmail.com', 'phone': '1234567890'}, 'linkedin_url' : 'https://www.linkedin.com/in/sushant-twayana-b4840a254/' }

patient1 = Patient(**patient_info)

# print(patient1)

insert_patient_data(patient1) 