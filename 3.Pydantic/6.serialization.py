from pydantic import BaseModel

class Address(BaseModel):

    city: str
    district: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'Sallagahri', 'district': 'Bhaktapur', 'pin': '40001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'sushant', 'age': 24, 'address': address1}

patient1 = Patient(**patient_dict)

temp1 = patient1.model_dump(include = ['name'])
temp2 = patient1.model_dump(exclude = ['name', 'gender'])
temp3 = patient1.model_dump(exclude={'address': ['district']})

temp = patient1.model_dump(exclude_unset=True)
# model_dump_json()

print(temp1)
print(temp2)
print(temp3)
print(temp)
print(type(temp))