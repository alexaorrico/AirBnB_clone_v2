#!/usr/bin/python3
""" starts api """
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)

HBNB_API_HOST = getenv("HBNB_API_HOST")
HBNB_API_PORT = getenv("HBNB_API_PORT")


@app.teardown_appcontext
def teardown(exception):
    """ i think it's supposed to be exception """
    """ a method that calls storage.close """
    storage.close()


@app.errorhandler(404)
def custom_404(error):
    """ Returns JSON 404 """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    if not HBNB_API_HOST:
        HBNB_API_HOST = "0.0.0.0"
    if not HBNB_API_PORT:
        HBNB_API_PORT = "5000"
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
