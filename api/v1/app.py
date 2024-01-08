#!/usr/bin/python3
"""Flask app entry point"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')


@app.teardown_appcontext
def close_storage(err):
    """calls close method"""
    storage.close()


if __name__ == '__main__':
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
