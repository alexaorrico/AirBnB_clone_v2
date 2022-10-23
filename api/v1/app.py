#!/usr/bin/python3
"""
module to start using api
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def exit(exception):
    ''' exit api in case of unexpected error '''
    storage.close()


@app.errorhandler(404)
def error404(e):
    """ instance of app to handle 404 errors """
    response = {"error": "Not found"}
    return make_response(jsonify(response), 404)

if __name__ == '__main__':
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000
    app.run(host=host, port=port)
