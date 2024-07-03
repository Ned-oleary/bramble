from flask import Blueprint
from typing import Tuple

bp = Blueprint("apollo", import_name="apollo_routes", url_prefix="/api/apollo")

@bp.route("/")
def default() -> Tuple[str, int]:
    return "Hello world", 201