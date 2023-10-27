#!/usr/bin/python3
"""Module contains flask app"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def closeStorage(exception):
    """Closes the storage session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """Custom 404 page not found json error message"""
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    useHost = getenv('HBNB_API_HOST', default='0.0.0.0')
    usePort = getenv('HBNB_API_PORT', default=5000)

    app.run(host=useHost, port=usePort, threaded=True)
