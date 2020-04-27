#!/usr/bin/python3
""" create  a instance Flask and register Blueprint """


from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """ down app and close storage """
    storage.close()


@app.errorhandler(404)
def not_found(message):
    """Handles the 404 status code"""
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
