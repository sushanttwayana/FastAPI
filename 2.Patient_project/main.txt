from fastapi import FastAPI, Pat h
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

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
def view_patient(patient_id: str):
    
    ### load all the patients
    
    data = load_data()
    
    
    if patient_id in data:
        return data[patient_id]
    
    else:
        return{'error': 'patient not found'}
    