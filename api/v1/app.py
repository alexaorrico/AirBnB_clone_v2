#!/usr/bin/python3
"""Rest api version 1"""

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


def create_app():
    """Create an configure the Flask app"""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(app_views)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    
    @app.teardown_appcontext
    def close_staorage(error):
        """close the app storage "DBStorage or FileStorage" """
        storage.close()


if __name__== "__main__":
    app = create_app()
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port)