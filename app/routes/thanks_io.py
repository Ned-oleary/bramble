from flask import Blueprint, request, jsonify
from ..utils.thanks_io_utils import THANKS_IO_SEND_URL, THANKS_IO_HEADERS
from typing import Tuple


bp = Blueprint("thanks_io", import_name = "thanks_io_routes", url_prefix = "/api/thanks_io")

@bp.route("/send/postcard", method = ["POST"])
def create_contacts() -> Tuple[str, int]: 
    data = request.get_json()
    response = request.post(url = THANKS_IO_SEND_URL, headers = THANKS_IO_HEADERS, json=data)
    if(response.status_code == response.codes.ok):
        return jsonify(response.json()), 201
    else:
        return response.text, 400