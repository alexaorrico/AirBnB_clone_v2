#!/usr/bin/python3
"""Status of api ApI V1"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """teardown appcontext"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a
    JSON-formatted 404 status code response
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or '0.0.0.0'
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True)
