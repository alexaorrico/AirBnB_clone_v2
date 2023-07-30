#!/usr/bin/python3
"""A simple REST API application to print status OK"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """A method to handle closing of application"""
    storage.close()

@app.errorhandler(404)
def error(e):
    """Return a 4O4 ERROR in json"""
    return jsonify({'error': 'Not found'})


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
