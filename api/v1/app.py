#!/usr/bin/python3
"""app.py to connect to API"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS

"""Create a Flask web application instance"""
app = Flask(__name__)

"""Register the "app_views" blueprint with the Flask app"""
app.register_blueprint(app_views)

"""Enable Cross-Origin Resource Sharing for the app"""
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

"""Define a teardown function to close the database
connection when the app context is torn down"""
@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
