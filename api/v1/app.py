#!/usr/bin/python3
"""this the module were flask is runned as server"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import make_response, jsonify
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """
    The function `close` is used to close a storage
    object and handle any exceptions that may occur.
    """
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    return make_response(jsonify({'error': 'Not found'}),
                         404)


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST") or "0.0.0.0",
            port=getenv("HBNB_API_PORT") or 5000, threaded=True)
