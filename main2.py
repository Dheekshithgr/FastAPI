from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round((self.weight/(self.height**2)),2)
    
    @computed_field
    @property
    def verdict_of_bmi(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<30:
            return 'Normal'
        else:
            return 'Obese'
        
        
patient_data={'id':"P001","name": "Ananya Verma", "city": "Guwahati", "age": 28, "gender": "female", "height": 1.65, "weight": 90.0,'city':'Gurgaun'}

patient1=Patient(**patient_data)

@app.post('/create')
def create_account(patient:Patient):
    
    data=load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    save_data(data)    

    return JSONResponse(status_code=201,content={'message':'Patient created successfully'})