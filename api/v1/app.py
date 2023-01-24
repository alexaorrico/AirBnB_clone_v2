#!/usr/bin/python3
""" Flask api to return status
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, origins='0.0.0.0')


@app.teardown_appcontext
def teardown(exception):
    """ destroys DB session in case of DB storage
        reloads objects in case of File Storage
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ response for 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    #  get host address
    host = getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'

    #  get port number
    port = getenv('HBNB_API_PORT')
    if port is None:
        port = '5000'

    app.run(host=host, port=port)
