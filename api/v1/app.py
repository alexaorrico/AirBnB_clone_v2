#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception):
    """Close the SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Handle the 404 errors """
    return make_response(jsonify({"error": "Not Found"}), 404)


if __name__ == "__main__":
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    else:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
