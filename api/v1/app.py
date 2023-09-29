#!/usr/bin/python3
import os
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views

HBNB_API_HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
HBNB_API_PORT = os.getenv('HBNB_API_PORT', 5000)
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(app):
    storage.close(app)


if __name__ == '__main__':
    app.run(host='HBNB_API_HOST', port=HBNB_API_PORT, threaded=True)
