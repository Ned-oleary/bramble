from dotenv import load_dotenv
import os

load_dotenv()

PEOPLE_MATCH_VALID_INPUTS = ["first_name", "last_name", "name", "email", 
                             "hashed_email", "organization_name", "domain",
                             "linkedin_url"]

PEOPLE_MATCH_URI = "https://api.apollo.io/v1/people/match"
PEOPLE_MATCH_URI_BULK = "https://api.apollo.io/api/v1/people/bulk_match"

COMPANY_MATCH_URI = "https://api.apollo.io/v1/organizations/enrich"
COMPANY_MATCH_URI_BULK = "https://api.apollo.io/api/v1/organizations/bulk_enrich"

MATCH_HEADERS : dict = {'Cache-Control': 'no-cache', 
                        'X-Api-Key': os.getenv("APOLLO_KEY")}

MATCH_HEADERS_BULK : dict = {'Content-Type': 'application/json', 
                                    'Cache-Control': 'no-cache', 
                                    'X-Api-Key': os.getenv("APOLLO_KEY")}

