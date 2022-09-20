#!/usr/bin/python3

"""Comments"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def call_close(exception):
    storage.close()


@app.errorhandler(404)
def handle_bad_request(exception):
    return {"error": "Not found"}, 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    if host is None:
        host = "0.0.0.0"
    port = os.getenv('HBNB_API_PORT')
    if port is None:
        port = 5000
    app.run(host=host, port=port, debug=False, threaded=True)
