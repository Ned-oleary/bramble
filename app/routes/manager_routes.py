from flask import Blueprint, jsonify, request
from ..utils.route_to_apollo_utils import enrich_company, search_people
from ..utils.manager_utils import strip_enrichment_json, strip_enrichment_json_to_dict

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

# ultimately would like this route to reduce to four function calls
@bp.route("/hello", methods = ["POST"])
def handler():
    processed_input = process_input_json(request.get_json())
    domains = processed_input["domains"]
    
    enriched_organizations = enrich_company(domains, "bulk") #dict
    enriched_organizations = strip_enrichment_json(enriched_organizations)
    enriched_org_lookup = strip_enrichment_json_to_dict(enriched_organizations) # returns domain-indexed dict of dicts
    
    print(enriched_org_lookup)
    
    people = search_people(gen_people_search_dict(domains = domains, job_titles = processed_input[job_titles]))

    join = [] # empty list of enriched people

    for person in people:
        print("looping:")
        print(person)
        if person["domain"] in enriched_org_lookup.keys():
            print("found domain: " + person["domain"])
            merge = {**person, **enriched_org_lookup[person["domain"]]}
            print("merge is")
            print(merge)
            join.append(merge) #add the dict that merges person with org

    print(join)

    return people, 200


def process_input_json(request: Response) -> dict[str]:
    print("calling process_input_json()")
    input_json = request.get_json()
    domains = (input_json["domainList"]).split(",")
    job_titles = (input_json["jobTitlesList"]).split(",")
    hubspot_use_only_new_contacts = input_json["useOnlyNewContacts"]
    max_dollars = input_from_front_end["maxDollars"]
    return_dict = {"domains": domains, "job_titles": job_titles, "max_dollars": max_dollars, "hubspot_use_only_new_contacts": hubspot_use_only_new_contacts}
    print(return_dict)
    return return_dict

def gen_people_search_dict(domains: list[dict[str]], job_titles: list[str], page: int = 1, per_page: int = 10):
    print("calling gen_people_search_dict()")
    people_search_dict = {
        "q_organization_domains" : '\n'.join(domains),
        "page": page,
        "per_page": per_page,
        "person_titles": job_titles
    }
    print(people_search_dict)
    return people_search_dict