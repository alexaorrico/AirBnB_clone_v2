#!/usr/bin/python3
"""
Flask app
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import environ

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    storage.close()

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.errorhandler(404)
def page_not_found(e):
    """handler for routes that don't exist"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
