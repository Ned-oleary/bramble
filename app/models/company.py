from uuid import uuid4
import warnings

class Company():
    def __init__(self):
        self.uuid: str = str(uuid4())
        self.apollo_id: str = ""
        self.hubspot_id: str = ""
        self.domain: str = ""
        self.website_url: str = ""
        self.name = ""
        self.linkedin_uid = ""
        self.raw_address = ""
        self.street_address = ""
        self.city = ""
        self.state = ""

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
            
    def set_values(self, **kwargs: str)-> None:
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ["uuid", "apollo_id", "hubspot_id"]:
                setattr(self, key, value)
            else:
                warnings.warn("Invalid key for set_values(): " + key)

    def to_dict(self, **kwargs: str) -> dict:
        return_dict = {}
        for keys, values in vars(self).items(): # messy to allow addition of new attributes
            if keys in kwargs.keys():
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




