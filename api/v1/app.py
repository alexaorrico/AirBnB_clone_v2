#!/usr/bin/python3
"""
Module For start a Flask web application
"""
from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views
from flask import make_response, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors that returns a JSON-formatted
    404 status code response.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host_env = getenv('HBNB_API_HOST')
    port_env = getenv('HBNB_API_PORT')
    app.run(host=host_env, port=port_env)
