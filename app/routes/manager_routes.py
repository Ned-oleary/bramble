from flask import Blueprint, jsonify, request, Response
from ..utils.route_to_apollo_utils import search_people, enrich_company
from ..utils.manager_utils import process_input_json, gen_people_search_dict
from ..utils.route_to_hubspot_utils import create_company, create_contact, get_companies, get_contacts, company_list_to_hs_list, people_list_to_hs_list
import asyncio

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

@bp.route("/hello", methods = ["POST"])
def handler():
    try:
        print("Hit backend")
        processed_input = process_input_json(request)
        input_domains = processed_input["domains"]
        input_job_titles = processed_input["job_titles"]

        print(input_domains)
        print(input_job_titles)
        if(input_domains == [''] or input_job_titles == ['']):
            raise ValueError 

        print("now processing hubspot data")
        existing_hubspot_people = asyncio.run(get_contacts()) # list of dicts
        existing_hubspot_companies = asyncio.run(get_companies()) # list of dicts
        print("finished processing hubspot data")

        apollo_enriched_organizations = (enrich_company(input_domains, "bulk"))["organizations"]
        apollo_people = (search_people(gen_people_search_dict(domains = input_domains, job_titles = input_job_titles))).get_json()

        # loop exists because person json will have *some* subset of org data as provided by apollo
        for person in apollo_people:
            org_data = person.pop("organization")
            for keys in org_data:
                value = org_data[keys]
                person["org_" + keys] = value

            for org in apollo_enriched_organizations:
                if org["primary_domain"] == person["org_primary_domain"]:
                    for keys in org:
                        values = org[keys]
                        person["org_" + keys] = values
        
        hubspot_input_companies = company_list_to_hs_list(apollo_enriched_organizations)
        for input_company in hubspot_input_companies:
            try:
                for existing_company in existing_hubspot_companies:
                    if input_company["properties"]["apollo_id"] == existing_company["apollo_id"]:
                        input_company["properties"]["hubspot_id"] = existing_company["hubspot_id"]
                        break
                    input_company["properties"]["hubspot_id"] = None
                if not input_company["properties"]["hubspot_id"]:
                    hubspot_response = create_company(input_company)
                    hubspot_response_json = hubspot_response.json()
                    input_company["properties"]["hubspot_id"] = hubspot_response_json["id"]

                for apollo_person in apollo_people:
                    if apollo_person["org_primary_domain"] == input_company["properties"]["domain"]:
                        apollo_person["org_hubspot_id"] = input_company["properties"]["hubspot_id"]
            except(Exception) as e:
                print("Error in input_company loop")
                raise e
        
        hubspot_input_people = people_list_to_hs_list(apollo_people) #returns a list of objects to push into hubspot
        for input_person in hubspot_input_people:
            should_create = True
            for hubspot_person in existing_hubspot_people:
                if input_person["properties"]["apollo_id"] == hubspot_person["apollo_id"]:
                    should_create = False
                    print("Found someone that already exists")
                    break
            if(should_create):
                hubspot_response = create_contact(input_person)
                print(hubspot_response)
    except ValueError:
        print("No input.")

    return jsonify({"message": "success"}), 200

