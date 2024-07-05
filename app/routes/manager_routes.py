from flask import Blueprint, jsonify, request
from ..utils.route_to_apollo_utils import enrich_company
#from ..utils.manager_utils import strip_enrichment_json

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

@bp.route("/hello", methods = ["POST"])
def handler():
    input_from_front_end = request.get_json()
    domains = (input_from_front_end["domainList"]).split(",") # need to comma separate raw string
    titles = input_from_front_end["jobTitlesList"].split(",") # need to comma separate raw string
    hubspot_use_only_new_contacts = input_from_front_end["useOnlyNewContacts"]
    max_dollars = input_from_front_end["maxDollars"]
    
    enriched_organizations = enrich_company(domains, "bulk")

    return enriched_organizations, 200