#!/usr/bin/python3
"""Create a variable app, instance of Flask"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """function teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def errorhandler(e):
    """Function that handles error 404"""
    error = {}
    error['error'] = "Not found"
    return jsonify(error), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
