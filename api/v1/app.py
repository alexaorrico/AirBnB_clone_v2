#!/usr/bin/python3
""" Flask """
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exception):
    """Close"""
    storage.close()

if __name__ == '__main__':
    my_host = os.getenv('HBNB_API_HOST')
    my_port = os.getenv('HBNB_API_PORT')
    app.run(host=my_host, port=my_port, threaded=True)
