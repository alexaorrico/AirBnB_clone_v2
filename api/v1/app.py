#!/usr/bin/python3
'''
Creating and starting API
'''

from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import Blueprint, Response
from os import getenv
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    '''Method to handle that calls storage.close()'''
    storage.close()


@app.errorhandler(404)
def handle_exception(e):
    return jsonify(
        {
            "error": "Not found"
        }), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
