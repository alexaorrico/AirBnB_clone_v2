#!/usr/bin/python3
"""Main Flask Application"""
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(err):
    """Close db Storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors that returns a
    JSON-formatted 404 status code response
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """Main function"""
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else "0.0.0.0"
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000
    app.run(host=host, port=port, threaded=True)
