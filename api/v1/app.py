#!/usr/bin/python3

""" app module """

from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error):
    storage.close()


@app.errorhandler(404)
def _handle_api_error(error):
    return jsonify(error="Not found")

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
