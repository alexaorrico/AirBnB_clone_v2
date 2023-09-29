#!/usr/bin/python3
"""registers all blueprint and run server"""
from api.v1.views import app_views
from api.v1.views import *
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

if __name__ == '__main__':
    host = getenv('HBHB_API_HOST')
    port = getenv('HBHB_API_PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000

    app.run(debug=True, host=host, port=port)
