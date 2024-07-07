from flask import Blueprint, jsonify, request
from ..utils.route_to_apollo_utils import enrich_company, search_people
from ..utils.manager_utils import strip_enrichment_json, strip_enrichment_json_to_dict

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

# need to break this up into a few utility functions -- too complicated at this point
@bp.route("/hello", methods = ["POST"])
def handler():
    processed_input = process_input_json(request.get_json())
    domains = processed_input["domains"]
    
    enriched_organizations = enrich_company(domains, "bulk") #dict
    enriched_organizations = strip_enrichment_json(enriched_organizations) # returns list
    enriched_org_lookup = strip_enrichment_json_to_dict(enriched_organizations) # returns domain-indexed dict of dicts


    #people is a dict 
    people = search_people(gen_people_search_dict(domains = domains, job_titles = processed_input[job_titles]))


    # note for 7/7 need to continue refactor -- this is a mess


    join = [] # empty list of enriched people

    for person in people:
        print(person)
        if person["domain"] in enriched_org_lookup.keys(): 
            merge = {**person, **enriched_org_lookup[person["domain"]]}
            join.append(merge) #add the dict that merges person with org

    print(join)

    return people, 200


def process_input_json(request: Response) -> dict[str]:
    input_json = request.get_json()
    domains = (input_json["domainList"]).split(",")
    job_titles = (input_json["jobTitlesList"]).split(",")
    hubspot_use_only_new_contacts = input_json["useOnlyNewContacts"]
    max_dollars = input_from_front_end["maxDollars"]
    return {"domains": domains, "job_titles": job_titles, "max_dollars": max_dollars, "hubspot_use_only_new_contacts": hubspot_use_only_new_contacts} 

def gen_people_search_dict(domains: list[str], job_titles: list[str], page: int = 1, per_page: int = 10):
    people_search_dict = {
        "q_organization_domains" : '\n'.join(domains),
        "page": page,
        "per_page": per_page,
        "person_titles": job_titles
    }
    return people_search_dict