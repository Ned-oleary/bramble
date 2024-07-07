from collections import defaultdict


def construct_domain_enrichment_json(domains: list[str]) -> dict[str]:
    return_dict = {
        "domains": domains,
        "choice": "bulk"
    }
    return return_dict

# this can definitely be simpler!!!
def strip_enrichment_json(enriched_organizations: dict[str], fields: list[str] = ["name", "street_address", "postal_code", "city", "state", "country",
                                               "linkedin_uid", "linkedin_url", "id", "primary_domain"], organization_domain: bool = True) -> list[str]:
    '''pass in a dict with a nested list, return the list, albeit with fewer fields'''    
    enriched_organizations = enriched_organizations["organizations"] #just get the nested list of dicts that's called "organizations"
    return_list = []
     for orgs in enriched_organizations:
        temp_dict = defaultdict(str) # for overwriting orgs
        for each_field in fields:
            temp_dict[each_field] = orgs[each_field] # {each_field: orgs[each_field], ... }
        return_list.append(temp_dict)
    return return_list

def strip_enrichment_json_to_dict(orgs_list: list[str]) -> dict[str]:
    '''takes list of dicts and changes to a dict of dicts, where domain is the key'''
    return_dict = defaultdict(dict)
    for orgs in orgs_list:
        domain = orgs.pop("domain")
        return_dict[domain] = orgs
    return return_dict