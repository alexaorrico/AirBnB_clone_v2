#!/usr/bin/python3
"""First api"""

from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ 404 not found handler """
    return make_response(jsonify(error='not found'), 404)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ closes current db session """
    storage.close()


if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST')
    api_port = getenv('HBNB_API_PORT')
    app.run(host=api_host if api_host else '0.0.0.0',
            port=api_port if api_port else 5000, threaded=True)
