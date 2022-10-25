#!/usr/bin/python3
"""Starts a Flask Application"""
from flask import Flask
from flask import jsonify
from flask import make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(e):
    """response to 404 errors"""
    return jsonify({
                    'error': 'Not found'
                   }), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host and port:
        app.run(host=host, port=port, threaded=True, debug=True)
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)


@app.teardown_appcontext
def tear_down():
    """closes the session on after a request"""
    storage.close()
