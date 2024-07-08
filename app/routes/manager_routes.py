from flask import Blueprint, jsonify, request, Response
from ..utils.route_to_apollo_utils import search_people
from ..utils.manager_utils import process_input_json, gen_people_search_dict
from ..utils.route_to_hubspot_utils import create_company

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

# ultimately would like this route to reduce to four function calls
@bp.route("/hello", methods = ["POST"])
def handler():
    processed_input = process_input_json(request)
    domains = processed_input["domains"]
    job_titles = processed_input["job_titles"]
    
    people = search_people(gen_people_search_dict(domains = domains, job_titles = job_titles))
    people = people.get_json()
    print("printing people 1")
    print("people")
    organizations = []

    for person in people:
        org_data = person.pop("organization")
        for keys in org_data:
            value = org_data[keys]
            person["org_" + keys] = value
            organizations.append({keys:value})
    
    print("printing people 2")
    print("people")

    # HS: create companies
        # HS: create contacts


    # generate subset for direct mailers

    # thanks.io automate sending
    
    return jsonify(people), 200


# HS properties -> company
# city = "city"
# company domain name = "domain"
# country = "country"
# linkedIn URL = "linkedin_company_page"
# postal code = "zip"
# record id = "hs_object_id"
# state/region = "state"
# street address = "address"
# apollo id = "apollo_id"


# HS properties -> person
# first name = "firstname"
# job title = "jobtitle"
# last name = "lastname"
# hubspot id = "hs_object_id"
# apollo id = "apollo_id"
# must make an association to company


# HS properties -> task
# make a POST request to /crm/v3/objects/tasks
# hs_timestamp # Unix or UTC
# hs_task_body # task notes
# hs_task_subject # title of the task
# hs_task_status #make COMPLETED
# hs_task_reminders # Unix timestamp in milliseconds for reminder notification
# must create an association # to company and contact