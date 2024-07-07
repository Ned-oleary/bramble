from flask import Blueprint, jsonify, request
from ..utils.route_to_apollo_utils import enrich_company, search_people
from ..utils.manager_utils import strip_enrichment_json, strip_enrichment_json_to_dict, process_input_json, gen_people_search_dict, merge_org_dict_and_people_list

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

# ultimately would like this route to reduce to four function calls
@bp.route("/hello", methods = ["POST"])
def handler():
    processed_input = process_input_json(request.get_json())
    domains = processed_input["domains"]
    
    enriched_organizations = enrich_company(domains, "bulk")
    enriched_organizations = strip_enrichment_json(enriched_organizations)
    enriched_org_lookup = strip_enrichment_json_to_dict(enriched_organizations) # returns domain-indexed dict of dicts
    
    print(enriched_org_lookup)
    
    people = search_people(gen_people_search_dict(domains = domains, job_titles = processed_input[job_titles]))

    merged_data = merge_org_dict_and_people_list(org_dict = enriched_org_lookup, people_list = people)

    return merged_data, 200
