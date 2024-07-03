from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate
from hubspot.crm.contacts.exceptions import ApiException
from dotenv import load_dotenv
import os

load_dotenv()

def init_hubspot(HUBSPOT_ACCESS_TOKEN: str = os.getenv("HUBSPOT_ACCESS_TOKEN")) -> HubSpot:
    hubspot_client: HubSpot = HubSpot(access_token="HUBSPOT_ACCESS_TOKEN")
    return hubspot_client

def try_create_contact(hubspot_client: HubSpot) -> None:
    try:
        simple_public_object_input_for_create = SimplePublicObjectInputForCreate(
            properties={"email": "email@example.com"}
        )
        api_response = hubspot_client.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=simple_public_object_input_for_create
        )
    except ApiException as e:
        print("Exception when creating contact: %s\n" % e)