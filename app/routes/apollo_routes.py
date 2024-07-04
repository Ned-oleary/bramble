from flask import Blueprint, jsonify, request
from typing import Tuple
from ..utils.apollo_utils import PEOPLE_MATCH_URI, PEOPLE_MATCH_URI_BULK, COMPANY_MATCH_URI, \
                                COMPANY_MATCH_URI_BULK, MATCH_HEADERS_NO_JSON, MATCH_HEADERS_JSON, \
                                PEOPLE_SEARCH_URI, APOLLO_MAX_RESULTS
import requests
from time import sleep

bp: Blueprint = Blueprint("apollo", import_name="apollo_routes", url_prefix="/api/apollo")

# processes 10 max at a time
@bp.route("/enrich/person", methods=["POST"])
def enrich_person() -> Tuple[dict, int]:
    data = request.get_json()

    if data["choice"] == "bulk":
        payload_dict = {"details": data["details"]}  
        response = requests.post(url=PEOPLE_MATCH_URI_BULK, headers=MATCH_HEADERS_JSON, json=payload_dict)
    else:
        response = requests.post(url=PEOPLE_MATCH_URI, headers=MATCH_HEADERS_NO_JSON, json=data["details"])  

    if response.status_code == 200:  # Use 200 for clarity, although requests.codes.ok is also correct
        return jsonify(response.json()), 201
    else:
        return response.text, response.status_code

# processes 10 max at a time
@bp.route("/enrich/company", methods = ["POST"])
def enrich_company() -> Tuple[dict, int]:
    data = request.get_json()  
    payload = {"domains": data["domains"]}

    if data["choice"] == "bulk":
        response = requests.post(url=COMPANY_MATCH_URI_BULK, headers=MATCH_HEADERS_JSON, json=payload)
    else:
        response = requests.get(url=COMPANY_MATCH_URI, headers=MATCH_HEADERS_JSON, params={"domain": data["domains"][0]})

    if response.status_code == 200:
        return jsonify(response.json()), 201
    else:
        return response.text, response.status_code
    
# Apollo will only show up to 100 results at a time
@bp.route("/search/people", methods = ["POST"])
def search_people():
    try:
        data = request.get_json()
        data["page"] = "1" # overwrite first call
        data["per_page"] = "100" # force Apollo to give us the max results
    
        response = requests.post(url = PEOPLE_SEARCH_URI, headers = MATCH_HEADERS_JSON, json = data)
        total_entries = int(response.json()["total_entries"])

        output = []
        output.append(response.json()["people"])

        if(total_entries > APOLLO_MAX_RESULTS):
            return jsonify("Too many results"), 400
    
        while (total_entries - len(output) > 0):
            data["page"] = str(int(data["page"]) + 1)
            response = requests.post(url = PEOPLE_SEARCH_URI, headers = MATCH_HEADERS_JSON, json = data)
            output.append(response.json()["people"])
            # probably want some backoff here
    
        return jsonify(output), 200
    
    except:
        return "Error", 400



        

