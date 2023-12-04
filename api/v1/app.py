#!/usr/bin/python3
""" Apllication using Flask """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def db_close(err):
    """ Closes the storage when app shutdown"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """Print 404 Error
    ---
    Responses:
      404:
        Description: not found
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", "5000"), threaded=True)
