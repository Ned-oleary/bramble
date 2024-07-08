from flask import Blueprint, jsonify, request, Response
from ..utils.route_to_apollo_utils import enrich_company, search_people
from ..utils.manager_utils import process_input_json, gen_people_search_dict

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

# ultimately would like this route to reduce to four function calls
@bp.route("/hello", methods = ["POST"])
def handler():
    processed_input = process_input_json(request)
    domains = processed_input["domains"]
    job_titles = processed_input["job_titles"]
    
    people = search_people(gen_people_search_dict(domains = domains, job_titles = job_titles))
    people = people.get_json()
    organizations = []

    for person in people:
        org_data = person.pop("organization")
        for keys in org_data:
            value = org_data[keys]
            person["org_" + keys] = value
            organizations.append({keys:value})


    # HS: create contacts

    # HS: create companies

    # generate subset for direct mailers

    # thanks.io automate sending
    
    return jsonify(people), 200
