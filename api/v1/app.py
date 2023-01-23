#!/usr/bin/python3

"""
Entry point for flask
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    """returns a JSON-formatted 404 status code response."""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(error):
    """teardown_appcontext"""
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True, debug=True)
