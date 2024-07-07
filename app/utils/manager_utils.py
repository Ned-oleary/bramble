from collections import defaultdict


def construct_domain_enrichment_json(domains: list[str]) -> dict[str]:
    return_dict = {
        "domains": domains,
        "choice": "bulk"
    }
    return return_dict

# this can definitely be simpler!!!
def strip_enrichment_json(pydict: dict[str], fields: list[str] = ["name", "street_address", "postal_code", "city", "state", "country",
                                               "linkedin_uid", "linkedin_url", "id", "primary_domain"], organization_domain: bool = True) -> dict[str]:
    pydict_org_list = pydict["organizations"]
    return_dict = defaultdict(list)
    for i in range(0, len(pydict_org_list)): # iterate over list of dicts
        temp_dict_copy = defaultdict(list)
        print(pydict_org_list[i])
        for field in fields: #for each desired output
            temp_dict_copy[field] = pydict_org_list[i][field]
        if(organization_domain):
            temp_dict_copy["domain"] = pydict_org_list[i]["primary_domain"]
        return_dict[i] = temp_dict_copy
    return return_dict
    
