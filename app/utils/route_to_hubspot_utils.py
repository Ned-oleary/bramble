from ..configs.hubspot_config import HubspotConfig
from flask import request, jsonify
from typing import Tuple
import requests

hs = HubspotConfig()

def create_contact() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.post(url = hs.CONTACTS_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

def create_company() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.post(url = hs.COMPANY_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

def get_contacts() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.get(url = hs.CONTACTS_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

def get_companies() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.get(url = hs.COMPANIES_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

def get_contacts() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.patch(url = hs.CONTACTS_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())

def get_companies() -> Tuple[str, int]:
    data = request.get_json()
    response = requests.patch(url = hs.COMPANIES_URI, headers = hs.HUBSPOT_DEFAULT_HEADERS, json = data)
    return jsonify(response.json())