#!/usr/bin/python3
"""
app file for the api
"""
from os import getenv
from models import storage
from flask import Blueprint, make_response
from flask import Flask, jsonify
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """ method to handle @app.teardown_appcontext """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns a JSON-formatted 404 status code response """
    return make_response(jsonify({'error': 'Not found'}), 404)
if __name__ == '__main__':
    """should not be executed when imported"""
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT,
            threaded=True, debug=True)
