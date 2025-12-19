from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse

class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description="ID of the patient", examples=['POO1'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(description="City where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt = 100, description="Current age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs")]

    
    @computed_field
    @property
    def bmi(self) -> float:
        
        bmi = round(self.weight / (self.height ** 2), 2)
        
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        
        if self.bmi < 18.5:
            return "Underweight"
        if self.bmi < 25:
            return "Normal"
        if self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity" 

## for updating the patient    
class PatientUpdate(BaseModel):
    
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Management System"}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}



### show all the details of the available patients
@app.get('/view')
def view():
    
    data = load_data()
    
    return data


### path parameters only with the specific patients
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the db', example='POO1')):
    
    ### load all the patients
    
    data = load_data()
    
    
    if patient_id in data:
        return data[patient_id]
    
    else:
        # return{'error': 'patient not found'}
        raise HTTPException(status_code= 404,detail = 'Patient not found')
    
### query parameter -> sort patients on the basis of input (sort_by) and sort_order
@app.get('/patient/sort')
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str =Query('asc', description = "Sort in ascending or descending order")):
    
     valid_fields = ['height', 'weight', 'bmi']
     
     if sort_by not in valid_fields:
         raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")
     
     if order not in ['asc', 'desc']:
         raise HTTPException(status_code=400, detail='Invalid order select either asc or desc')
     
     data = load_data()
     sort_order = True if order == 'desc' else False
     
    #  sorted(data.values(), key = lambda x: x.get('height', 0), reverse=True) ## reverse=True descending order False ascending order
    
     sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=sort_order) 
     
     return sorted_data
 
 
 
#### ========================= create new endpoint to create new patient============================================
@app.post('/patient')
def create_patient(patient: Patient): ## getting patient data from Pydantic model with validation 
     
     ### load existing data
     data = load_data()
     
     ## check whether the patient already exists
     if patient.id in data:
         raise HTTPException(status_code=400, detail="Patient already exists")
     
     ### add new patient to our json

     ##convert pydantic object to  dictonary first
     data[patient.id] = patient.model_dump(exclude=['id'])
     
     ## save again into the json file
     save_data(data)
     
     return JSONResponse(status_code=201, content={'message': "patient created successfully"})
 
 
 
#####  Update or edit the existing patients on the db
@app.put('/patient/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    
    data = load_data()
    
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]
    
    ## convert pydnatic object to dict
    updated_patient_info = patient_update.model_dump(exclude_unset=True) ## only extracting the field set by the client not all 
    
    for key, value in updated_patient_info.items():  ### loop in updated one only 
        
        existing_patient_info[key] = value  #### updating in the existing json file
        
    # existing_patient_info --> pydantic object -->> calculate new bmi and verdict --->> to get the new bmi and verdict -->> updated bmi +verdict 
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
        
    # existing_patient_info --> pydantic object -->> calculate new bmi and verdict --->> to get the new bmi and verdict -->> updated bmi +verdict -->>  pydantic object -->> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
    
    ## add this data to data  
    data[patient_id] = existing_patient_info
    
    ## save data
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message': "Patient updated successfuly"})


##### Delete the existing patients on the basis of id 
@app.delete('/patient/{patient_id}')
def delete_patient(patient_id:str):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message': 'patient deleted successfully'})    