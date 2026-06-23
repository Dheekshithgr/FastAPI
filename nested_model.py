from pydantic import BaseModel,EmailStr

class Address(BaseModel):
    
    city:str
    state:str
    pincode:int
    
class Patient(BaseModel):
    name:str
    age:int
    address:Address
    email:EmailStr
    
address_data={'city':'Gundlupet','state':'Karnataka','pincode':571111}

address=Address(**address_data)

patient_data={'name':'ABCD','age':29,'address':address,'email':'abcd@gmail.com'}
patient1=Patient(**patient_data)

print(patient1)