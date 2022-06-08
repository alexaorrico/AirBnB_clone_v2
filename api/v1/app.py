#!/usr/bin/python3
"""RESTfull API for the project 
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources=r"/*")
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            "error": "Not found"
        }
    )

@app.teardown_appcontext
def teardown_app(exc):
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST"), port=getenv("HBNB_API_PORT"), threaded=True)