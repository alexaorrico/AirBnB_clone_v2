#!/usr/bin/python3
""" Starts a Flask web application for blueprints """
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ App closes storage when closed """
    storage.close()


@app.errorhandler(404)
def error_handler(err):
    """ This method handle the error 404 response """
    return jsonify({"error": "Not found"}), 404


hosts = getenv('HBNB_API_HOST', '0.0.0.0')
ports = getenv('HBNB_API_PORT', '5000')

if __name__ == "__main__":
    app.run(host=hosts, port=ports, threaded='True', debug=True)
