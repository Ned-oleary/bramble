from flask import Blueprint, jsonify, request
from typing import Tuple
from ..configs.apollo_config import ApolloConfig
import requests

apollo = ApolloConfig()

# Apollo will only show up to 100 results at a time
def search_people(query: dict[str, int]) -> dict[str]:
    print("Calling search_people() utility")
    print(query)
    
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



        

