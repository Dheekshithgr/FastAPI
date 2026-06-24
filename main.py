from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,Literal,Optional


def load_data():
    with open("patients.json",'r') as f:
        data=json.load(f)
        
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

app=FastAPI()

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
        
class PatientUpdate(BaseModel):
    
    name:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    city:Annotated[Optional[str],Field(default=None)]
    gender:Annotated[Optional[Literal['male','female']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None)]
    weight:Annotated[Optional[float],Field(default=None)]
        
@app.get('/')
def hello():
    return {'message':'HELLO'}

@app.get('/about')
def about():
    return {'Dheekshith':'We have nothing to say about him'}

@app.get('/view')
def view():
    data =load_data()
    return data

@app.get('/patient/{patient_id}')
def id_check(patient_id:str = Path(...,description="Enter the patient id",example="P001")):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found!")

@app.get('/sort')
def sort_patient(sort_by:str=Query(...,description="Sort on the basis of height,weight,bmi"),order :str=Query('asc',description="Sort in ascending or descending(default=asc)")):
    valid_fields=['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Select from {valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Please select from asc and desc")
    
    data=load_data()
    
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse= True if order=='desc' else False)
    
    return sorted_data

@app.post('/create')
def create_account(patient:Patient):
    
    data=load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    save_data(data)    

    return JSONResponse(status_code=201,content={'message':'Patient created successfully'})

@app.put('/edit')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found!")
    existing_patient_info=data[patient_id]
    
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value
    
    existing_patient_info['id']=patient_id    
    patient_pydantic=Patient(**existing_patient_info)
    
    existing_patient_info=patient_pydantic.model_dump(exclude_unset=True)
    
    data[patient_id]=existing_patient_info
    
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'Patient updated successfully'})

@app.delete('/delete')
def delete_patient(patient_id:str):
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':"Patient deleted successfully"})