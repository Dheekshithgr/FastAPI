from fastapi import FastAPI,Path,HTTPException,Query
import json

def load_data():
    with open("patients.json",'r') as f:
        data=json.load(f)
        
    return data

app=FastAPI()

@app.get('/')
def hello():
    return {'message':'Hello World!'}

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