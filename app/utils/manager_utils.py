
def construct_domain_enrichment_json(domains: list[str]) -> dict[str]:
    return_dict = {
        "domains": domains,
        "choice": "bulk"
    }
    return return_dict

def strip_enrichment_json(pydict: dict[str], fields: list[str] = ["name", "street_address", "postal_code", "city", "state", "country",
                                               "linkedin_uid", "linkedin_url", "id", "primary_domain"], organization_domain: bool = True) -> dict[str]:
    print(pydict)
    return_dict = {}
    for i in range(0, len(pydict)):
        print(i)
        temp_dict = {}
        print(pydict[i])
        for key in fields:
            temp_dict[key] = pydict[i][key]
        if(organization_domain):
            temp_dict["domain"] = pydict[i]["organization"]["primary_domain"]
        return_dict[i] = temp_dict
    return return_dict
    
