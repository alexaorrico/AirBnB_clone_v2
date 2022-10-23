#!/usr/bin/python3
'''first endpoint (route) to return the status of your API'''

import code
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import Blueprint, jsonify, make_response
import os

app = Flask(__name__)
app.register_blueprint(app_views)
@app.teardown_appcontext
def closestorage(code):
    '''teardown context'''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    '''Return 404 error'''
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
