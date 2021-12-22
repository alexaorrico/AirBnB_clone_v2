#!/usr/bin/python3
"""Script checking status of API"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Call on storage.close that handles teardowns"""
    storage.close()


@app.errorhandler(404)
def not_found_error(e):
    '''
    this method displays a json 404 error
    '''
    not_found_text = {"error": "Not found"}
    return (jsonify(not_found_text), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    """if host == None:
        host = 0.0.0.0"""
    port = getenv("HBNB_API_PORT")
    """if port == None:
        port = 5000"""
    app.run(host=host, port=port, threaded=True)
