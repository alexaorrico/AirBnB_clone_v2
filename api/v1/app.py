#!/usr/bin/python3
"""
create a variable app, instance of Flask
import storage from models
import app_views from api.v1.views
register the blueprint app_views to your Flask instance app
declare a method to handle @app.teardown_appcontext
that calls storage.close()
"""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)

CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exception):
    '''TearDown:
    closes the storage on app context teardown
    removes the current SQLAlchemy Session object after each request
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''404:
    return errmsg `Not Found`
    '''
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
