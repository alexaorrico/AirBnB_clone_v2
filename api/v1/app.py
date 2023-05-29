#!/usr/bin/python3
"""
create a variable app, instance of flask
import storage from models
import app_views from api.v1.views
register the blueprint app_views to your Flask instance app
declare a method to handle @app.teardown_appcontext that
calls storage.close().
inside if __name__ == "__main__":, run your Flask server
(variable app) with:
host = environment variable HBNB_API_HOST or 0.0.0.0 if not defined
port = environment variable HBNB_API_PORT or 5000 if not defined
threaded=True
"""
from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exception=None):
    """close storage"""
    return storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
