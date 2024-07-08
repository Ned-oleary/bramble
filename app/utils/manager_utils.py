from __future__ import annotations
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Response

# TODO: nest this under the process
def construct_domain_enrichment_json(domains: list[str]) -> dict[str]:
    print("calling construct_domain_enrichment_json()")
    return_dict = {
        "domains": domains,
        "choice": "bulk"
    }
    return return_dict


# TODO: nest these into the enrich util

# TODO: rename this
def strip_enrichment_json(enriched_organizations: dict[str], fields: list[str] = ["name", "street_address", "postal_code", "city", "state", "country",
                                               "linkedin_uid", "linkedin_url", "id", "primary_domain"], organization_domain: bool = True) -> list[str]:
    '''pass in a dict with a nested list, return the list, albeit with fewer fields'''    
    enriched_organizations = enriched_organizations["organizations"] #just get the nested list of dicts that's called "organizations"
    return_list = []
    for orgs in enriched_organizations:
        temp_dict = {} # for overwriting orgs
        for each_field in fields:
            temp_dict[each_field] = orgs[each_field] # {each_field: orgs[each_field], ... }
        return_list.append(temp_dict)
    return return_list

#TODO: rename this 
def strip_enrichment_json_to_dict(orgs_list: list[str]) -> dict[str]:
    '''takes list of dicts and changes to a dict of dicts, where domain is the key'''
    return_dict = {}
    for orgs in orgs_list:
        print("==================")
        print("ORGS:")
        print(orgs)
        domain = orgs["primary_domain"]
        print("popped orgs")
        print(orgs)
        return_dict[domain] = orgs
    return return_dict

def process_input_json(request: flask.Response) -> dict[str]:
    print("calling process_input_json()")
    input_json = request.get_json()
    domains = (input_json["domainList"]).split(",")
    job_titles = (input_json["jobTitlesList"]).split(",")
    hubspot_use_only_new_contacts = input_json["useOnlyNewContacts"]
    max_dollars = input_json["maxDollars"]
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

# note: realized people data includes organization data anyway
# can simplify the code by a much bigger margin now 
def merge_org_dict_and_people_list(org_dict: dict[dict[str]], people_list = list[dict[str]]) -> list[dict[str]]:
    '''used solely to combine the enriched org data from apollo with the searched people from apollo'''
    
    join = []
    print(org_dict)

    # not the most efficient code in the world, but it's a bit clearer than what used to be here
    # and we're not handling so much data that it reeeeally matters, anyway
    for org_domain in org_dict:
        org_data = org_dict[org_domain]
        for index in range(0, len(people_list)): 
            if people_list[index]["organization"]["primary_domain"] == org_domain:
                person = people_list.pop(index)
                person["org_name"] = org_data["name"]
                person["org_street_address"] = org_data["street_address"]
                person["org_postal_code"] = org_data["postal_code"]
                person["org_linkedin_id"] = org_data["linkedin_uid"]
                person["org_apollo_id"] = org_data["id"]
                person["org_primary_domain"] = org_data["primary_domain"]
                join.append(person)
    
    return join