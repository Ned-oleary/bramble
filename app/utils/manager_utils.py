
def construct_domain_enrichment_json(domains: list[str]) -> dict[str]:
    return_dict = {
        "domains": domains,
        "choice": "bulk"
    }
    return return_dict

# def strip_enrichment_json(pydict: dict[str], fields: list[str] = ["name", "street_address", "postal_code", "city", "state", "country",
#                                                "linkedin_uid", "linkedin_url", "id"]) -> dict[str]:
#     return_dict = {}
#     for key, value in pydict:
#         if key in fields:
#             return_dict[key] = value
#     return return_dict
    
