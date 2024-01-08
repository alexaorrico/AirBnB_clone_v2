#!/usr/bin/python3
"""
This is the base file for my api
"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(args=None):
    # This func closes the storage
    storage.close()


@app.errorhandler(404)
def not_found(error):
    # This method returns a json error message when a url is not found
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
