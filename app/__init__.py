from flask import Flask
from .models import init_models # may be able to remove this
from .routes import register_routes
#from flask_cors import CORS

def create_app() -> Flask:
    app = Flask(__name__)
    init_models(app)
    register_routes(app)
    #app.config.from_object("config.Config")
    #CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})
    return app
