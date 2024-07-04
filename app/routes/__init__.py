from typing import TYPE_CHECKING
from .apollo_routes import bp as ar
from .thanks_io import bp as thx

if TYPE_CHECKING:
    from flask import Flask

def register_routes(app: 'Flask') -> None:
    app.register_blueprint(ar)
    app.register_blueprint(thx)
    return None
