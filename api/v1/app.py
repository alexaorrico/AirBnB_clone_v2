#!/usr/bin/python3
""" module to run flask app """
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS


HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


def port_host(HBNB_API_HOST, HBNB_API_PORT):
    """ set up host and port variables """
    if not HBNB_API_HOST:
        HBNB_API_HOST = '0.0.0.0'
    if not HBNB_API_PORT:
        HBNB_API_PORT = '5000'


@app.teardown_appcontext
def teardown(exception):
    """ handle app teardowns with storage close """
    storage.close()


@app.errorhandler(404)
def error_404(self):
    """ handle error_404 """
    error_dict = {"error": "Not found"}
    return make_response(jsonify(error_dict), 404)


if __name__ == "__main__":
    port_host(HBNB_API_HOST, HBNB_API_PORT)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, debug=True, threaded=True)
