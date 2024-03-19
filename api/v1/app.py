#!/usr/bin/python3
"""Returns API status"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
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
    host1 = getenv('HBNB_API_HOST', default='0.0.0.0')
    port1 = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host1, port=port1, threaded=True)