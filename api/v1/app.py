#!/usr/bin/python3
"""create a variable app, instance of Flask"""
from flask import Flask, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.register_blueprint(app_views)



@app.teardown_appcontext
def teardown_db(exception):
    """close storage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """error 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host, port, threaded=True)
