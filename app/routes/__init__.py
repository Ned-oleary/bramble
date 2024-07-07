from typing import TYPE_CHECKING
from .manager_routes import bp as manager

if TYPE_CHECKING:
    from flask import Flask

def register_routes(app: 'Flask') -> None:
    app.register_blueprint(manager)
    return None
