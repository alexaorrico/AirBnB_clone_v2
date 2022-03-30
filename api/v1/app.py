#!/usr/bin/python3
"""
create a variable app, instance of Flask
register the blueprint app_views to your Flask instance app
"""
from models import storage
from os import getenv
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

if not host:
    host = "0.0.0.0"

if not port:
    port = 5000

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """
    closes session
    """
    storage.close()


@app.errorhandler(404)
def not_found_404(error):
    """
    returns error
    """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
