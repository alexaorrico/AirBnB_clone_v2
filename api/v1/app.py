#!/usr/bin/python3
''' 
variable app instance of flask
it contains method to handle @app.teardown_context
'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    '''teardown method meant for storage'''
    storage.close()

if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST') 
    app_port = os.getenv('HBNB_API_PORT')
    if app_host is None:
        app_host = '0.0.0.0'
    if app_port is None:
        app_port = 5000
    app.run(host=app_host, port=int(app_port))