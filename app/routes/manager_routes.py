from flask import Blueprint, jsonify, request
from ..utils.route_to_apollo_utils import enrich_company, search_people
from ..utils.manager_utils import strip_enrichment_json

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

# need to break this up into a few utility functions -- too complicated at this point
@bp.route("/hello", methods = ["POST"])
def handler():

    #we get the domains and the titles from the frontend
    input_from_front_end = request.get_json()
    domains = []
    domains.extend((input_from_front_end["domainList"]).split(",")) # need to comma separate raw string
    titles = input_from_front_end["jobTitlesList"].split(",") # need to comma separate raw string
    hubspot_use_only_new_contacts = input_from_front_end["useOnlyNewContacts"]
    max_dollars = input_from_front_end["maxDollars"]
    
    people_search_domains = '\n'.join(domains)
    enriched_organizations = enrich_company(domains, "bulk")
    enriched_organizations = strip_enrichment_json(enriched_organizations) #should work now

    
    people_search_dict = {
        "q_organization_domains": people_search_domains,
        "page": 1,
        "per_page": 5,
        "person_titles": titles,
    }

    people = search_people(people_search_dict) # we get the people from search

    enriched_org_lookup = {
        org["domain"]: {"name": org["name"], "address": org["address"]} # getting stuck here
        for org in enriched_organizations # iterate over list -> convert into a dict keyed by a domain
    }

    for orgs in enriched_organizations:
        enriched_org_lookup["domain"] = {}


    join = [] # empty list of enriched people

    for person in people:
        print(person)
        if person["domain"] in enriched_org_lookup: # this will probably fail
            merge = {**person, **enriched_org_lookup[person["domain"]]}
            join.append(merge) #add the dict that merges person with org

    print(join)

    return people, 200