#!/usr/bin/python3
"""
Starts the flask app.py
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


host_env = getenv("HBNB_API_HOST", "0.0.0.0")
port_env = getenv("HBNB_API_PORT", "5000")

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_con(error):
    """closes the database connection"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """creates a 'Not found'"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=host_env, port=port_env, threaded=True)
