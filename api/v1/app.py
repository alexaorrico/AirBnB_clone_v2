#!/usr/bin/python3
"""
    API
"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', '5000'))
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_app(code):
    '''
       Method  Handles teardown
    '''
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
