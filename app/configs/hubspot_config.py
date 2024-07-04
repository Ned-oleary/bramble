import os

class HubspotConfig():
    BASE_URI = 'https://api.hubapi.com'
    ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
    HUBSPOT_DEFAULT_HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN,
                            'Content-Type': 'application/json'}
    CONTACTS_URI = BASE_URI + '/crm/v3/objects/contacts'
    COMPANIES_URI = BASE_URI + '/crm/v3/objects/companies'

