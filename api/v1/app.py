#!/usr/bin/python3
""" AirBnB_clone's Flask api app """

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

HBNB_API_HOST = getenv('HBNB_API_HOST', default='0.0.0.0')
HBNB_API_PORT = getenv('HBNB_API_PORT', default='5000')

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage engine"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 status code response"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
