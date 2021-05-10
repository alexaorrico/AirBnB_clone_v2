#!/usr/bin/python3
"""It’s time to start the HBNB API!"""
import os
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views

if __name__ == "__main__":

    app = Flask(__name__)
    app.register_blueprint(app_views)

    @app.teardown_appcontext
    def close_app():
        storage.close()

    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = os.getenv('HBNB_API_PORT', default='5000')

    app.run(host=host, port=port, threaded=True)
