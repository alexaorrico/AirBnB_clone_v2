#!/usr/bin/python3
"""a module as an API"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    """a function to call storage.close()"""
    return storage.close()


@app.errorhandler(404)
def not_found(error):
    """a function to handle default 404 HTML response
    with a JSON response"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", "0.0.0.0")
    api_port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=api_host, port=api_port, threaded=True)
