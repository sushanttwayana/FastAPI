from pydantic import BaseModel

class Address(BaseModel):

    city: str
    district : str
    postal_code: str
    house_no: int



class Patient(BaseModel):
    
    name: str
    gender: str
    age: int
    # address: 'house no 23, Road 123, Sallaghari, Bhaktapur, 40011' ## complex data type
    address: Address
    
    
address_dict = {'city': 'Sallaghari', 'district': 'Bhaktapur', 'postal_code': '40011', 'house_no':23 }

address1 = Address(**address_dict)

patient_dict = {'name': 'Sushant Twayana', 'gender': 'male', 'age': 35, 'address': address1}


patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.postal_code)

# ============================================================================================ #

# Better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use Vitals in multiple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically—no extra work needed

# ============================================================================================ #