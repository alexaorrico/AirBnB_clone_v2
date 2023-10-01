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
    app.register_blueprint(app_views)

    @app.errorhandler(404)
    def not_found(error):
        """Handles 404 not found"""
        result = {"error": "Not found"}
        return jsonify(result), 404

    @app.teardown_appcontext
    def close_staorage(error):
        """close the app storage "DBStorage or FileStorage" """
        storage.close()

    return app


if __name__ == "__main__":
    app = create_app()
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port)
