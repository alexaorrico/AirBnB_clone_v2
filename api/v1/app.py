#!/usr/bin/python3
"""Creating the API and returning the status"""

from models import storage
from api.v1.views import app_views
from flask import Flask, render_template, make_response, jsonify
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(exception):
    """Tears down by calling storage.close"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST",
                        default="0.0.0.0"),
            port=getenv("HBNB_API_PORT",
                        default="5000"),
            threaded=True)
