from typing import Union
from uuid import uuid4
import warnings

class Person:
    def __init__(self) -> None:
        self.uuid = str(uuid4())
        self.apollo_id: str = None
        self.hubspot_id: str = None
        self.first_name: str = None
        self.last_name: str = None
        self.name: str = None
        self.title: str = None
        self.github_url: str = None
        self.email: str = None
        self.hashed_email: str = None
        self.organization_name: str = None
        self.organization_apollo_id: str = None
        self.organization_hubspot_id: str = None
        self.linkedin_url: str = None
        self.state: str = None
        self.city: str = None
        self.country: str = None
        self.domain: str = None
        self.departmental_head_count = {}
    
    def get_id(self, query:str = "uuid") -> str:
        match query:
            case "uuid":
                return self.uuid
            case "apollo":
                return self.apollo_id
            case "hubspot":
                return self.apollo_id
            case _:
                raise ValueError("Invalid argument to get_id()")
    
    def set_id(self, setter:str) -> None:
        match setter:
            case "apollo":
                self.apollo_id = setter
            case "hubspot":
                self.hubspot_id = setter
            case _:
                raise ValueError("Invalid argument to set_id()")
            
    def set_values(self, **kwargs: Union[str, dict])-> None:
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ["uuid", "apollo_id", "hubspot_id"]:
                setattr(self, key, value)
            else:
                warnings.warn("Invalid key for set_values(): " + key)

    def to_dict(self, input_list: list) -> dict:
        return_dict = {}
        for keys, values in vars(self).items(): # messy to allow addition of new attributes
            if keys in input_list:
                return_dict[keys] = values
        return return_dict
    
    def print(self) -> None:
        print("==================================")
        for keys, values in vars(self).items():
            if(values):
                if(type(values).__name__ != "dict"):
                    print(keys + ": " + values)
                else:
                    print(keys + ": dict")
        print("================================-")

def generate_test_person() -> Person:
    person = Person()
    person.set_values(
        city = "San Francisco",
        state =  "California",
        name = "Ned OLeary",
        domain = "ssoready.com",
        email = "ned.oleary@ssoready.com"
    )
    return person






        
        



