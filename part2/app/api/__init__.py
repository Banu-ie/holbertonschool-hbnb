from flask import Flask
from app.api.v1 import api as api_v1

def create_app():
    app = Flask(__name__)

    api_v1.init_app(app)

    return app