#!/usr/bin/python3
"""api app"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=getenv('HBNB_API_PORT', default='5000'), threaded=True)
