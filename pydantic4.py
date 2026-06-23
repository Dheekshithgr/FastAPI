#computed_fields

from pydantic import BaseModel,EmailStr,AnyUrl,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:str
    email:EmailStr
    url:AnyUrl
    age:int
    height:float
    weight:float
    married:Optional[bool]=False
    allergies:Optional[List[str]]
    contacts:Dict[str,str]
    
    @computed_field
    @property
    def bmi(self,) -> float:
        return round(self.weight/(self.height**2),2)
        
def create_account(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.contacts['name'])
    print(patient.married)
    print(patient.allergies)
    print('BMI :',patient.bmi)
    print('Account created successfully!')

def update_account(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.contacts['name'])
    print(patient.married)
    print(patient.allergies)
    print('Account updated successfully!')
    
patient_info={'name':'Abc','age':50,'weight':66.6,'allergies':['pollen','dust'],'contacts':{'name':'Xyz','phone':'989775'},'height':1.75,'email':'abcd@hdfc.com','url':'https://google.com'}

patient1=Patient(**patient_info)

create_account(patient1)