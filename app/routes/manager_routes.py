from flask import Blueprint, jsonify, request
from ..utils.route_to_apollo_utils import enrich_company, search_people
#from ..utils.manager_utils import strip_enrichment_json

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

@bp.route("/hello", methods = ["POST"])
def handler():
    input_from_front_end = request.get_json()
    domains = []
    domains.extend((input_from_front_end["domainList"]).split(",")) # need to comma separate raw string
    titles = input_from_front_end["jobTitlesList"].split(",") # need to comma separate raw string
    hubspot_use_only_new_contacts = input_from_front_end["useOnlyNewContacts"]
    max_dollars = input_from_front_end["maxDollars"]
    
    people_search_domains = '\n'.join(domains)
    enriched_organizations = enrich_company(domains, "bulk")
    
    people_search_dict = {
        "q_organization_domains": people_search_domains,
        "page": 1,
        "per_page": 100,
        "person_titles": ["software engineer", "account executive"],
    }

    people = search_people(people_search_dict)
    print(people)

    return people, 200