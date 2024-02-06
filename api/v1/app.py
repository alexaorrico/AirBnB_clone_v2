#!/usr/bin/python3
"""
contains the main application
"""
from flask_cors import CORS
from flasgger import Swagger
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(obj):
    """calls close()"""
    storage.close()


@app.errorhandler(404)
def no_found_page(error):
    """Page not found in json format"""
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': 'This is the api that was created for the hbnb restful api project,\
    all the documentation will be shown below',
    'uiversion': 3}

Swagger(app)


if __name__ == "__main__":

    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = os.getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
