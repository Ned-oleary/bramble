from flask import Blueprint, jsonify, request
from typing import Tuple
from ..configs.apollo_config import ApolloConfig
import requests

apollo = ApolloConfig()

# Apollo will only show up to 100 results at a time
def search_people(query: dict[str, int]) -> dict[str]:    
    all_people = []
    num_total_people = 0
    num_loops = 0
    num_people_captured = 0
    while (num_loops == 0 or num_people_captured < num_total_people):
        response = requests.post(url = apollo.PEOPLE_SEARCH_URI, headers = apollo.MATCH_HEADERS_JSON, json = query)
        response_data = response.json()
        if not num_loops:
            num_total_people = int(response_data["pagination"]["total_entries"])
        num_loops += 1
        new_people = response_data["people"]
        all_people.extend(new_people)
        num_people_captured += len(new_people)
    return jsonify(all_people)


def enrich_company(domains: list[str], type_arg: str) -> dict[str]:
    domains = {"domains": domains}
    if(type_arg == "bulk"):
        response = requests.post(url=apollo.COMPANY_MATCH_URI_BULK, headers=apollo.MATCH_HEADERS_JSON, json=domains)
    else:
        response = requests.get(url=apollo.COMPANY_MATCH_URI, headers=apollo.MATCH_HEADERS_JSON, params={"domain": domains[0]})
    if response.status_code == 200: #problem here
        return response.json()  # Make sure to convert to JSON
    else:
        return response.text
    



        

