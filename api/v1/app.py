#!/usr/bin/python3
"""
    return the Status of your API
"""

from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """will closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def ops_404(error):
    """this will create a handler for 404 errors"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
