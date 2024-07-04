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

@bp.route("/enrich/person", methods = ["POST"])
def enrich_person() -> Tuple[str, int]:
    data: dict = request.get_json()
    payload_dict: dict = {}
    if(data["choice"]) == "bulk":
        payload_dict["details"] = data["details"]
        url = PEOPLE_MATCH_URI_BULK
    else:
        payload_dict = data["details"]
        url = PEOPLE_MATCH_URI
    response = requests.post(url=PEOPLE_MATCH_URI, headers=PEOPLE_MATCH_HEADERS, data=payload_dict)
    if response.status_code == requests.codes.ok:
        return response.json(), 201
    else:
        return response.text, response.status_code

@bp.route("/enrich/company", methods = ["POST"])
def enrich_company() -> Tuple[str, int]:
    data = requests.json()
    payload = data["domains"]
    if data["choice"] == "bulk":
        pass
    else:
        pass
        
        

