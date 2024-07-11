from ..configs.hubspot_config import HubspotConfig
from flask import request, jsonify
from typing import Tuple
import requests
import aiohttp

hs = HubspotConfig()

#need revision
def create_contact(people_list: list[dict[str]]) -> dict[str]:
    response = requests.post(url = hs.CONTACTS_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = people_list)
    print(response.json())
    return response.json()

def create_company(company_list: list[dict[str]]) -> dict[str]:
    response = requests.post(url = hs.COMPANIES_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = company_list)
    print(response.json())
    return response.json()

async def get_contacts(property_list: list[str] = ["apollo_id", "firstname", "lastname"]) -> dict[str]:
    print("calling get_contacts()")
    url = hs.CONTACTS_URI

    query_dict = {"properties" : property_list}

    return_list = []
    async with aiohttp.ClientSession() as session:
        keep_getting = True
        while keep_getting:
            print("looping")
            response = await session.get(url = url, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = query_dict)
            response_results = await response.json()
            response_results = response_results["results"]
            print(response_results)
            for results in response_results:
                try:
                    return_list.append(results["apollo_id"])
                except(Exception) as e:
                    print("had an issue with indexing apollo_id")
                    pass
                    
            try:
                next_url = await response.json()
                next_url = next_url["paging"]["next"]["link"]
                url = next_url
            except(Exception) as e:
                print("finished looping")
                keep_getting = False
    
    return return_list



    return response.json()

def get_companies(property_list: list[str] = ["apollo_id", "domain"]) -> dict[str]:
    print("calling get_companies()")
    query_dict = {"properties" : []}
    for properties in property_list:
        (query_dict["properties"]).append(properties)
    response = requests.get(url = hs.COMPANIES_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = query_dict)
    print(response.json())
    return response.json()


def company_list_to_hs_list(company_list: list[dict[str]]) -> list[dict[str]]:
    print("calling company_list_to_hs_list()")
    return_company_list = []
    for company in company_list:
        company = {
            "properties":
            {
                "name": company["name"],
                "domain": company["primary_domain"],
                "address": company["street_address"],
                "city": company["city"],
                "state": company["state"],
                "country": company["country"],
                "zip": company["postal_code"],
                "linkedin_company_page": company["linkedin_url"],
                "apollo_id" : company["id"]
            }
        }
        return_company_list.append(company)
    return return_company_list # can hubspot not tolerate multiple companies?

# wonder if hubspot is smart enough to make the association for me...\
# currently hoping that hs_email_domain works
# because I don't know the 
def people_list_to_hs_list(people_list: list[dict[str]]) -> list[dict[str]]:
    print("calling people list to hs list")
    return_people_list = []
    for person in people_list:
        print(person)
        person = {
            "properties":{
                "firstname": person["first_name"],
                "lastname": person["last_name"],
                "jobtitle": person["title"],
                "address": person["org_street_address"],
                "city": person["org_city"],
                "state": person["org_state"],
                "country": person["org_country"],
                "zip": person["org_postal_code"],
                "apollo_id" : person["id"],
                }
            ,
            "associations": [
                {
                    "to":{
                        "id" : person["org_hubspot_id"]

                    },
                    "types":[
                        {
                            "associationCategory" : "HUBSPOT_DEFINED",
                            "associationTypeId": 279
                        }
                    ]
                }
            ]
        }
        return_people_list.append(person)
    print("return_people_list:")
    print(return_people_list)
    return return_people_list

