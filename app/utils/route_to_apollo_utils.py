from flask import Blueprint, jsonify, request
from typing import Tuple
from ..configs.apollo_config import ApolloConfig
import requests
from time import sleep

apollo = ApolloConfig()

# processes 10 max at a time
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

# processes 10 max at a time
def enrich_company(domains: list[str], type: str) -> Tuple[dict, int]:
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
def search_people():
    try:
        data = request.get_json()
        data["page"] = 1 # always start with the first page
        data["per_page"] = apollo.APOLLO_MAX_RESULTS_PER_PAGE # force Apollo to max the output per call
    
        all_people = []
        num_total_people = 0

        num_loops = 0
        num_people_captured = 0
    
        while (num_loops == 0 or num_people_captured < num_total_people):
            response = requests.post(url = apollo.PEOPLE_SEARCH_URI, headers = apollo.MATCH_HEADERS_JSON, json = data)
            response_data = response.json()

            if not num_loops:
                num_total_people = int(response_data["total_entries"])
            num_loops += 1

            new_people = response_data["people"]
            all_people.extend(new_people)
            num_people_captured += len(new_people)

            # probably want some backoff here

        return jsonify(all_people), 200
    
    except:
        return "Search people endpoint failed", 400



        

