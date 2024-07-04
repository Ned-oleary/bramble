from flask import Blueprint, jsonify, request
from typing import Tuple, TYPE_CHECKING
from dotenv import load_dotenv
from ..models.person import generate_test_person
from ..utils.apollo_utils import PEOPLE_MATCH_VALID_INPUTS, PEOPLE_MATCH_URI, PEOPLE_MATCH_URI_BULK, COMPANY_MATCH_URI, COMPANY_MATCH_URI_BULK
import requests, os

load_dotenv()

if TYPE_CHECKING:
    from flask import Flask
    from ..models.person import Person, generate_test_person

PEOPLE_MATCH_HEADERS : dict = {'Cache-Control': 'no-cache', 
                        'X-Api-Key': os.getenv("APOLLO_KEY")}

PEOPLE_MATCH_BULK_HEADERS : dict = {'Content-Type': 'application/json', 
                                    'Cache-Control': 'no-cache', 
                                    'X-Api-Key': os.getenv("APOLLO_KEY")}

bp: Blueprint = Blueprint("apollo", import_name="apollo_routes", url_prefix="/api/apollo")

@bp.route("/enrich/person", methods=["POST"])
def enrich_person() -> Tuple[dict, int]:
    data = request.get_json()

    if data["choice"] == "bulk":
        payload_dict = {"details": data["details"]}  
        response = requests.post(url=PEOPLE_MATCH_URI_BULK, headers=PEOPLE_MATCH_BULK_HEADERS, json=payload_dict)
    else:
        response = requests.post(url=PEOPLE_MATCH_URI, headers=PEOPLE_MATCH_HEADERS, json=data["details"])  

    if response.status_code == 200:  # Use 200 for clarity, although requests.codes.ok is also correct
        return jsonify(response.json()), 201
    else:
        return response.text, response.status_code

@bp.route("/enrich/company", methods = ["POST"])
def enrich_company() -> Tuple[dict, int]:
    data = request.get_json()  # Correct way to get JSON data
    payload = {"domains": data["domains"]}  # Ensure payload is correctly formatted as JSON

    if data["choice"] == "bulk":
        response = requests.post(url=COMPANY_MATCH_URI_BULK, headers=PEOPLE_MATCH_BULK_HEADERS, json=payload)
    else:
        response = requests.get(url=COMPANY_MATCH_URI, headers=PEOPLE_MATCH_BULK_HEADERS, params={"domain": data["domains"][0]})

    if response.status_code == 200:
        return jsonify(response.json()), 201
    else:
        return response.text, response.status_code
        

