#!/usr/bin/python3
"""
First endpoint (route) will be to
return the status of the API
"""

import json
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)


app_host = getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    """ handling the not_found """
    response = e.get_response()
    response.data = json.dumps({"error": "Not found"})
    response.content_type = "application/json"
    return response


@app.teardown_appcontext
def teardown_db(Exception):
    """ closes the storage on teardown """
    storage.close()


if __name__ == '__main__':
    """ Run the server """
    app_host = getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
