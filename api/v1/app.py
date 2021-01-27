#!/usr/bin/python3
"""
Module for hbnb API api
"""
from flask import Flask, render_template, Blueprint, jsonify
from models import storage
from api.v1.views from app_views
app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appconext
def teardown_api():
    """After query return ends current session"""
    storage.close()


if __name__ == "__main__":
    host = getenv(HBNB_API_HOST='0.0.0.0')
    port = int(getenv(HBNB_API_PORT='5000'))
    app.run(host, port, threaded=True)
