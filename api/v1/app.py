#!/usr/bin/python3
"""
blue print module for api
contain all the routes
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

"""create a variable app, instance of Flask"""
app = Flask(__name__)

"""register the blueprint app_views to your Flask instance app"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(debug=True, threaded=True, host=host, port=port)
