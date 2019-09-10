#!/usr/bin/python3
# Flask module to return status of API
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv, environ


app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def clean_up(self):
    '''closes storage'''
    storage.close()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    if environ.get('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    if environ.get('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
