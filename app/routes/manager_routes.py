from flask import Blueprint, jsonify, request, Response
from ..utils.route_to_apollo_utils import search_people, enrich_company
from ..utils.manager_utils import process_input_json, gen_people_search_dict
from ..utils.route_to_hubspot_utils import create_company, create_contact, get_companies, get_contacts, company_list_to_hs_list, people_list_to_hs_list
import asyncio

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

# ultimately would like this route to reduce to four function calls
@bp.route("/hello", methods = ["POST"])
def handler():
    processed_input = process_input_json(request)
    domains = processed_input["domains"]
    job_titles = processed_input["job_titles"]

    # should change companies to fetch IDs + evaluate domain matches
    existing_hubspot_people = asyncio.run(get_contacts()) # list here of just apollo IDs
    existing_hubspot_companies = asyncio.run(get_companies()) # for now, just a list of apollo IDs

    enriched_organizations = enrich_company(domains, "bulk")
    enriched_organizations = enriched_organizations["organizations"]

    people = search_people(gen_people_search_dict(domains = domains, job_titles = job_titles))
    people = people.get_json()

    # realize this isn't ideal, but I think it's fine anyway
    # loop exists because person json will have *some* subset of org data as provided by apollo
    for person in people:
        org_data = person.pop("organization")
        for keys in org_data:
            value = org_data[keys]
            person["org_" + keys] = value

        for org in enriched_organizations:
            if org["primary_domain"] == person["org_primary_domain"]:
                for keys in org:
                    values = org[keys]
                    person["org_" + keys] = values
    
    # should rename this at some point
    hs_companies = company_list_to_hs_list(enriched_organizations)

    # this is fucking stupid, BUT as far as I can tell... 
    # this is the only way to bulk create using the hubspot API
    # should collapse this functionality into some tidier code with backoff shortly
    for company in hs_companies:
        if company["properties"]["apollo_id"] not in existing_hubspot_companies: # this should change later
            try:
                print("creating_person!")
                response = create_company(company)
                print(response)
                for person in people:
                    if person["org_primary_domain"] == company["properties"]["domain"]:
                        person["org_hubspot_id"] = response["id"]
            except:
                print("had an issue with " + company["properties"]["name"])

    # ah this returns an error right now -- not just a nice-to-have to pull hubspot IDs into 
    # the get_companies method :()
    hs_people = people_list_to_hs_list(people) #returns a list of objects to push into hubspot
    for person in hs_people:
        if(person["properties"]["apollo_id"] not in existing_hubspot_people):
            print("creating person!")
            hs_response = create_contact(person)
            print(hs_response)
        else:
            print("found someone that already exists!")

    # # generate subset for direct mailers

    # # thanks.io automate sending

    return jsonify({"test": "test"}), 200

