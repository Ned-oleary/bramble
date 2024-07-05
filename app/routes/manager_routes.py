from flask import Blueprint, jsonify, request

bp = Blueprint("manager", import_name="manager-routes", url_prefix="/handler")

@bp.route("/hello", methods = ["POST"])
def handler():
    input_from_front_end = request.get_json()
    domains = (input_from_front_end["domainList"]).split(",") # need to comma separate raw string
    titles = input_from_front_end["jobTitlesList"].split(",") # need to comma separate raw string
    hubspot_use_only_new_contacts = input_from_front_end["useOnlyNewContacts"]
    max_dollars = input_from_front_end["maxDollars"]

    # apollo people search here
    
    return jsonify({"domains": domains}), 201