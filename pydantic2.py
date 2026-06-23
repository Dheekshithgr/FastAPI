#field_validator--> Used to validate single field(eg. age)

from pydantic import BaseModel,EmailStr,AnyUrl,field_validator
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
    
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icici.com']
        
        domain_name=value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()
    
    @field_validator('age',mode='after')
    @classmethod
    def validate_age(cls,value):
        if 0<value<100:
            return value
        else:
            raise ValueError('age should be between 0 and 100')
    
    
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