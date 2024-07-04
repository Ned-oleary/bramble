from dotenv import load_dotenv
import requests, os

load_dotenv()
BASE_URL = 'https://api.hubapi.com'
ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
HUBSPOT_DEFAULT_HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN,
                            'Content-Type': 'application/json'}


STUB = '/crm/v3/objects/contacts'

# def test_hubspot():
#     response = requests.get(url = URL, headers = HUBSPOT_DEFAULT_HEADERS) 
#     response_json = response.json()
#     print(response_json)



### create a contact record
test_dict = {}
test_dict_properties = {
    "email": 'a_new_example_email@hubspot.com',
    'firstname': 'example',
    'lastname': 'example',
}
test_dict["properties"] = test_dict_properties
# test_dict["associations"] = 

def create_contact():
    response = requests.post(url = BASE_URL + STUB, headers = HUBSPOT_DEFAULT_HEADERS, 
                             json = test_dict)
    print(test_dict)
    print(response.json())

