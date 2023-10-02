#!/usr/bin/python3
""" API """

import os
from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Handles storage calls """
    storage.close()

@app.errorhandler(NotFound)
def handle_not_found_error(error):
    """ Custom error handle for 404 errors"""
    response = {
        "error": "Not found"
    }
    return jsonify(response), 404

if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = getenv("HBNB_API_PORT", '5000')
    app.run(host=HOST, port=PORT, threaded=True)