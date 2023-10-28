#!/usr/bin/python3
"""Return the status of your API"""
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """Close the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def ops_404(error):
    """Create a handler for 404 errors"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
