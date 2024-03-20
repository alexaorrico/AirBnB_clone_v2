#!/usr/bin/python3
"""Returns API status"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    '''exit storage'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """json 404"""
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
