#!/usr/bin/python3
"""Contains a Flask web application API .
Endpoint (route) will be to return the status of your API
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# creating a Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.errorhandler(404)
def page_not_found(error):
    '''Handles the 404 HTTP error code.'''
    return {"error": "Not found"}, 404

@app.errorhandler(400)
def page_not_found(error):
    '''Handles the 400 HTTP error code.'''
    message = error.description
    return message, 400

@app.teardown_appcontext
def close(ctx):
    '''The Flask app/request context end event listener.'''
    storage.close()

if os.getenv("HBNB_API_HOST"):
    host = os.getenv("HBNB_API_HOST")
else:
    host = "0.0.0.0"

if os.getenv("HBNB_API_PORT"):
    port = int(os.getenv("HBNB_API_PORT"))
else:
    port = 5000

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)