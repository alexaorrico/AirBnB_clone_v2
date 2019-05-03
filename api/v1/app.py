#!/usr/bin/python3
"""Entry point for HolbertonBnB API calls."""
from os import getenv
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flasgger import Swagger, swag_from
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

template = {
    "swagger": "2.0",
    "info": {
        "title": "HolbertonBnB",
        "description": "RESTful API for HolbertonBnB",
    }
}
swagger = Swagger(app, template=template)


@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formatted 404 status code response."""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_storage(exc):
    """Closes the storage session after every request."""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", default="0.0.0.0"),
        port=getenv("HBNB_API_PORT", default="5000"),
        threaded=True
    )
