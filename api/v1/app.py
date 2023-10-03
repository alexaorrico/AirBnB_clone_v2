#!/usr/bin/python3
""" API """

import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """ Handles storage calls """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """ Custom error handle for 404 errors"""
    response = {
        "error": "Not found"
    }
    return jsonify(response), 404

if __name__ == "__main__":
    HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = os.getenv("HBNB_API_PORT", '5000')
    app.run(host=HOST, port=PORT, threaded=True)