#!/usr/bin/python3
""" Starts a Flask web app
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, Blueprint, jsonify
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def end_session(exception):
    """ ends the current session
    """
    return storage.close()


@app.errorhandler(404)
def not_found(self):
    """handle a 404 error"""
    json_not_found = (jsonify({'error': 'Not found'}), 404)
    return json_not_found


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
