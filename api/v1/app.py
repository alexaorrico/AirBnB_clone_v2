#!/usr/bin/python3
''' Sets up a Flask '''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from api.v1.views import state_views
from api.v1.views import city_views
import os
import json


app = Flask('__name__')

app.register_blueprint(app_views)
app.register_blueprint(state_views)
app.register_blueprint(city_views)


@app.teardown_appcontext
def handler(error):
    ''' Handles teardown '''
    storage.close()


@app.errorhandler(404)
def handler(error):
    ''' Handles 404 error '''
    return json.dumps({"error": "Not found"}, indent=4), 404


@app.errorhandler(400)
def handler(error):
    ''' Handles 404 error '''
    return jsonify(error=str(error)), 400


if __name__ == '__main__':
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True)
