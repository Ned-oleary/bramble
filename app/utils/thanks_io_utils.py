from flask import Blueprint, request, jsonify
from ..configs.thanksio_config import THANKS_IO_SEND_URL, THANKS_IO_HEADERS
from typing import Tuple

def create_contacts() -> Tuple[str, int]: 
    data = request.get_json()
    response = request.post(url = THANKS_IO_SEND_URL, headers = THANKS_IO_HEADERS, json=data)
    if(response.status_code == response.codes.ok):
        return jsonify(response.json())
    else:
        return response.text