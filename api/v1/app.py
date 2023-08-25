#!/usr/bin/python3
"""
start of my API, work towards endpoint(route) to return
status of my application
"""
from os import getenv

from flask import Flask, make_response, jsonify

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_storage(error=None):
    """calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') and getenv('HBNB_API_PORT'):
        app.run(host=getenv('HBNB_API_HOST'),
                port=int(getenv('HBNB_API_PORT')), threaded=True)
    else:
        app.run(host='0.0.0.0', port=500, threaded=True)
