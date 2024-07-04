from ..configs.hubspot_config import HubspotConfig
from flask import Blueprint, request, jsonify
from typing import Tuple
import requests

hs = HubspotConfig()
bp = Blueprint(name = "hubspot", import_name="hubspot_routes", url_prefix="/api/hubspot")

bp.route("/create_contact", methods = ["POST"])
def create_contact() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.post(url = hs.CONTACTS_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

bp.route("/create_company", methods = ["POST"])
def create_company() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.post(url = hs.COMPANY_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

bp.route("/get_contacts", methods = ["GET"])
def get_contacts() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.get(url = hs.CONTACTS_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

bp.route("/get_companies", methods = ["GET"])
def get_companies() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.get(url = hs.COMPANIES_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

bp.route("/update_contacts", methods = ["POST"])
def get_contacts() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.patch(url = hs.CONTACTS_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

bp.route("/update_companies", methods = ["POST"])
def get_companies() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.patch(url = hs.COMPANIES_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())