#!/usr/bin/python3
"""
hey
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv

app = Flask(__name__)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """after each request"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ override of the default 404 page"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    """
    Main Flask App
    """
    app.run(host=host, port=port, threaded=True)
