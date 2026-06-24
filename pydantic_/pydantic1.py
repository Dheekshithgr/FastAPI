from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:Annotated[str,Field(max_length=50,description='Name should be a string and less than 50 characters',examples=['Amit','Sumit'])]
    email:EmailStr
    url:AnyUrl
    age:int=Field(gt=0,lt=100)
    weight:Annotated[float,Field(gt=0,strict=True)]
    married:Annotated[bool,Field(description='Is the patient married or not?',default=False)]
    allergies:Optional[List[str]]=None
    contacts:Dict[str,str]
    
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
    
patient_info={'name':'Abc','age':50,'weight':66.6,'allergies':['pollen','dust'],'contacts':{'name':'Xyz','phone':'989775'},'email':'abcd@gmail.com','url':'https://google.com'}

patient1=Patient(**patient_info)

create_account(patient1)