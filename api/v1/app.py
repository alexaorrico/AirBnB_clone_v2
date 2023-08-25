#!/usr/bin/python3
"""
Flask App
"""
from models import storage
from api.v1.views import app_views
import os
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)


# Register the blueprint containing the API routes
app.register_blueprint(app_views)


# Setup CORS to allow requests from any origin
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


# Teardown app context to close database connection
@app.teardown_appcontext
def close_db(error):
    """
    Closes storage
    """
    storage.close()


@app.errorhandler(404)
def not_found():
    """
    404 status error handler
    """
    return make_response(jsonify({"error": "Not found"}), 404)
    

if __name__ == "__main__":
    """
    Main Function
    """
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
    