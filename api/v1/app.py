#!/usr/bin/python3
"""This runs the flask app"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_session(exception):
    '''This method closes a storage session'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''This returns a JSON response with 404 status'''
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
