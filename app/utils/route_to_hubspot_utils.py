from ..configs.hubspot_config import HubspotConfig
from flask import request, jsonify
from typing import Tuple
import requests
import aiohttp
import time

hs = HubspotConfig()

def create_contact(people_list: list[dict[str]]) -> dict[str]:
    response = requests.post(url = hs.CONTACTS_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = people_list)
    return response.json()

def create_company(company_list: list[dict[str]]) -> dict[str]:
    response = requests.post(url = hs.COMPANIES_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = company_list)
    return response.json()

# need to pass desired properties as params, comma separated
async def get_contacts(property_list: list[str] = ["apollo_id", "firstname", "lastname"]) -> list[dict[str]]:
    wait_time = 1
    url = hs.CONTACTS_URI + "?properties="+ "%2C".join(property_list)
    return_list = []
    async with aiohttp.ClientSession() as session:
        keep_getting = True
        while keep_getting:
            response = await session.get(url = url, headers = hs.HUBSPOT_DEFAULT_HEADERS)
            response_json = await response.json()
            response_status = response.status
            response_headers = response.headers
            if response_status == 429 or (response_status == 400 and 'X-HubSpot-RateLimit-Remaining' in response_headers):
                print("Getting rate limited on contacts getter!")
                time.sleep(wait_time)
                wait_time = 2 * wait_time
            elif response_status == 200:
                wait_time = wait_time / 2
                response_results = response_json["results"]
                for results in response_results:
                    apollo_id = results["properties"]["apollo_id"]
                    if(apollo_id):
                        return_list.append({"apollo_id": apollo_id})
                try:
                    next_url = response_json["paging"]["next"]["link"]
                    url = next_url
                except KeyError:
                    keep_getting = False
            else:
                raise("Unexpected response code " + response_status)
    return return_list

async def get_companies(property_list: list[str] = ["apollo_id", "domain"]) -> list[dict[str]]:
    wait_time = 1
    url = hs.COMPANIES_URI + "?properties="+ "%2C".join(property_list)
    
    return_list = []
    async with aiohttp.ClientSession() as session:
        keep_getting = True
        while keep_getting:
            response = await session.get(url = url, headers = hs.HUBSPOT_DEFAULT_HEADERS)
            response_json = await response.json()
            response_status = response.status
            response_headers = response.headers

            if response_status == 429 or (response_status == 400 and 'X-HubSpot-RateLimit-Remaining' in response_headers):
                print("Getting rate limited on companies getter!")
                time.sleep(wait_time)
                wait_time = 2 * wait_time
            elif response_status == 200:
                wait_time = wait_time / 2
                response_results = response_json["results"]
                for results in response_results:
                    apollo_id = results["properties"]["apollo_id"]
                    domain = results["properties"]["domain"]
                    hubspot_id = results["id"]
                    return_list.append({"apollo_id": apollo_id, "domain": domain, "hubspot_id": hubspot_id})
                try:
                    next_url = response_json["paging"]["next"]["link"]
                    url = next_url
                except KeyError:
                    keep_getting = False
            else:
                raise("Unexpected response code " + response.status)
    return return_list


def company_list_to_hs_list(company_list: list[dict[str]]) -> list[dict[str]]:
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

def people_list_to_hs_list(people_list: list[dict[str]]) -> list[dict[str]]:
    return_people_list = []
    for person in people_list:
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
    return return_people_list

