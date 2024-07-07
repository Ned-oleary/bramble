from flask import Blueprint, jsonify, request
from typing import Tuple
from ..configs.apollo_config import ApolloConfig
import requests

apollo = ApolloConfig()

# processes 10 max at a time
# should change just to use the bulk APi
# won't get used, but should keep just in case
def enrich_person() -> Tuple[dict, int]:
    data = request.get_json()

    if data["choice"] == "bulk":
        payload_dict = {"details": data["details"]}  
        response = requests.post(url=apollo.PEOPLE_MATCH_URI_BULK, headers=apollo.MATCH_HEADERS_JSON, json=payload_dict)
    else:
        response = requests.post(url=apollo.PEOPLE_MATCH_URI, headers=apollo.MATCH_HEADERS_NO_JSON, json=data["details"])  

    if response.status_code == 200:  # Use 200 for clarity, although requests.codes.ok is also correct
        return jsonify(response.json()), 201
    else:
        return response.text, response.status_code

# should get rid of this and make it only use the bulk api -- otherwise it's just a pain in the ass
# processes 10 max at a time
def enrich_company(domains: list[str], type: str) -> dict[str]:
    print("calling enrich_company()")
    print(domains)

    domains = {"domains": domains}

    if(type == "bulk"):
        print("calling bulk endpoing")
        response = requests.post(url=apollo.COMPANY_MATCH_URI_BULK, headers=apollo.MATCH_HEADERS_JSON, json=domains)
    else:
        print("calling single endpoint")
        response = requests.get(url=apollo.COMPANY_MATCH_URI, headers=apollo.MATCH_HEADERS_JSON, params={"domain": domains[0]})
    print(response.json())

    if response.status_code == 200: #problem here
        return response.json()  # Make sure to convert to JSON
    else:
        return response.text
    
# Apollo will only show up to 100 results at a time
# we can definitely simplify this a bit
def search_people(query: dict[str, int]) -> dict[str]:
    print("Calling search_people() utility")
    print(query)

    query["page"] = 1 
    #query["per_page"] = 5 
    
    all_people = []
    num_total_people = 0

    num_loops = 0
    num_people_captured = 0
    
    while (num_loops == 0 or num_people_captured < num_total_people):
        response = requests.post(url = apollo.PEOPLE_SEARCH_URI, headers = apollo.MATCH_HEADERS_JSON, json = query)
        response_data = response.json()
        print("looping " + str(num_loops))

        if not num_loops:
            num_total_people = int(response_data["pagination"]["total_entries"])
            print("total_entries: " + str(num_total_people))
        num_loops += 1

        new_people = response_data["people"]
        all_people.extend(new_people)
        num_people_captured += len(new_people)

        # probably want some backoff here

        # for testing reasons; REMOVE
        if(num_loops > 1):
            print("breaking loop")
            break

    return jsonify(all_people)



        

