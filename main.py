from  fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json
from fastapi.responses import JSONResponse

app=FastAPI()

class PatientUpdate(BaseModel):
    
    name:Optional[str]=None
    city: Optional[str]=None
    age: Annotated[Optional[int], Field(gt=0, lt=120)]=None
    gender: Optional[Literal['male', 'female', 'others']]=None
    height: Annotated[Optional[float], Field(gt=0)]=None
    weight: Annotated[Optional[float], Field(gt=0)]=None
    
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
    def bmi(self)->float:
        return round((self.weight/(self.height**2)),2)
    
    @computed_field
    @property
    def bmi_verdict(self)->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get('/')
def greet():
    return {'message':'Hello World!'}

@app.get('/view')
def view_patients():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def get_patient_id(patient_id:str=Path(...,description="Enter patient id to check",example="P001")):
    
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    return data[patient_id]

@app.get('/sort')
def sort_user(sort_by:str=Query(...,description='Sort on the basis of height,weight,bmi'),order:str=Query('asc',description='ascending or descending')):
    valid_criteria=['height','weight','bmi']
    
    if sort_by not in valid_criteria:
        raise HTTPException(status_code=400,detail=f"Select from {valid_criteria}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Please select from asc and desc")
    
    data=load_data()
    
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=True if order=='desc' else False)
    
    return sorted_data

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'Patient deleted successfully'})
    
@app.post('/create')
def create_user(patient:Patient):
    data=load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':"Patient created successfully"})

@app.put('/update')
def update_user(patient_id:str,patient:PatientUpdate):
    
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found!")
    existing_patient_info=data[patient_id]
    
    pydantic_dict=patient.model_dump(exclude_unset=True)
    
    existing_patient_info.update(pydantic_dict)
    
    existing_patient_info['id']=patient_id
        
    updated_patient_info=Patient(**existing_patient_info)
    
    data[patient_id]=updated_patient_info.model_dump(exclude=['id'])
    
    save_data(data)

    return JSONResponse(status_code=200,content={'message':'Patient updated successfully'})