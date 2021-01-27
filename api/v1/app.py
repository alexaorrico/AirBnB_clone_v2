#!/usr/bin/python3
"""
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(exception):
    storage.close()

if __name__ == "__main__":

    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
