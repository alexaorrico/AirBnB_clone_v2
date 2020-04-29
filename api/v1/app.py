#!/usr/bin/python3
""" app """
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
import os
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(err):
    """ method """
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """ handle for 404 errors """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(port), threaded=True)
