from pydantic import BaseModel,EmailStr

class Address(BaseModel):
    
    city:str
    state:str='Karnataka'
    pincode:int
    
class Patient(BaseModel):
    name:str
    age:int
    address:Address
    email:EmailStr
    
address_data={'city':'Gundlupet','pincode':571111}

address=Address(**address_data)

patient_data={'name':'ABCD','age':29,'address':address,'email':'abcd@gmail.com'}
patient1=Patient(**patient_data)

temp=patient1.model_dump(include=['name','age'])
print(type(temp))
print(temp)
temp1=patient1.model_dump_json(exclude={'address':{'pincode'}})
temp1=patient1.model_dump_json(exclude_unset=True)#all default values which user didnt provide will be excluded
print(type(temp1))
print(temp1)
