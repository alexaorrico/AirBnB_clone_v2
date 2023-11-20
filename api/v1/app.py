#!/usr/bin/python3
""" Getting started with API Stats """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

# Adds flask and blueprint
app = Flask(__name__)
app.register_blueprint(app_views)

# Adds CORS
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


# Adds teardown
@app.teardown_appcontext
def teardown_db(close):
    """ Removes current storage object"""
    storage.close()

# Adds 404 handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

# Adds host and port
host = getenv("HBNB_API_HOST", default="0.0.0.0")
port = getenv("HBNB_API_PORT", default="5000")


# Avoides import execution
if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)