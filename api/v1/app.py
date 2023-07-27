#!/usr/bin/python3
"""
Module containing Flask API
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
# HTTP access control (CORS)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(obj):
    """Method that removes current session"""
    storage.close()


@app.errorhandler(404)
def page_not_foun(error):
    """Method that handles 404 status in JSON fromat"""
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': 'Python back-end API webserver Flask',
    'uiversion': 3}

Swagger(app)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)
