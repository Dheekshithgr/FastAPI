#model_validator-->Used to validate multiple fields(eg. age,married)

from pydantic import BaseModel,EmailStr,AnyUrl,model_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:str
    email:EmailStr
    url:AnyUrl
    age:int
    weight:float
    married:Optional[bool]=False
    allergies:Optional[List[str]]
    contacts:Dict[str,str]
    
    @model_validator(mode='after')
    def check_emergency(cls,model):
        if model.age>60 and 'emergency' not in model.contacts:
            raise ValueError('Patient above 60 must have emergency contact')
        else :
            return model
    
    
def create_account(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.contacts['name'])
    print(patient.married)
    print(patient.allergies)
    print('Account created successfully!')

def update_account(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.contacts['name'])
    print(patient.married)
    print(patient.allergies)
    print('Account updated successfully!')
    
patient_info={'name':'Abc','age':50,'weight':66.6,'allergies':['pollen','dust'],'contacts':{'name':'Xyz','phone':'989775'},'email':'abcd@hdfc.com','url':'https://google.com'}

patient1=Patient(**patient_info)

create_account(patient1)