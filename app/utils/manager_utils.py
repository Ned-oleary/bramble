from __future__ import annotations
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Response

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