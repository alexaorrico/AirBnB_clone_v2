#!/usr/bin/python3
"""flask app"""

from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(excp):
    """Closes storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """page not found"""
    return make_response(jsonify({'error': 'Not found'}), 400)


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST") or '0.0.0.0',
            port=getenv("HBNB_API_PORT") or '5000', threaded=True)
