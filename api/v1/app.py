#!/usr/bin/python3
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(close):
    ''' Closes current storage session '''
    storage.close()


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    if (getenv('HBNB_API_HOST')):
        host = getenv('HBNB_API_HOST')
    if (getenv('HBNB_API_PORT')):
        port = int(getenv('HBNB_API_PORT'))
    app.run(host=host, port=port, threaded=True)
