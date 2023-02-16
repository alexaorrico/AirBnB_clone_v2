#!/usr/bin/python3
"""
This is an endpoint to return the status of the API
"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import environ as env

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, origins=["0.0.0.0"])


@app.teardown_appcontext
def teardown_app(exception):
    """ Closes the database request after each request"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns the error code 404 if wrong url """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = env.get("HBNB_API_HOST", "0.0.0.0")
    port = int(env.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
