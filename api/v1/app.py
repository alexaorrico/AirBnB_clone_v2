#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, Blueprint, render_template


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def stor_close(err):
    """ calls storage close """
    storage.close()

if __name__ == "__main__":
    """ Run the Flask server (variable app) """
    host = environ.get('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    port = environ.get('HBNB_API_PORT')
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
