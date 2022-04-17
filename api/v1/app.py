#!/usr/bin/python3
""" contains root flask application"""
from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def reload_storage(err):
    """reloads a storage"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """if no endpoints found"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(getenv('HBNB_API_HOST') or '0.0.0.0',
            getenv('HBNB_API_PORT') or 500,
            threaded=True)
