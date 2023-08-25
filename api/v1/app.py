#!/usr/bin/python3
"""Script to start the API"""


from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, jsonify
from flask_cors import CORS



app = Flask(__name__)

app.register_blueprint(app_views)


# Create a CORS instance with permissive settings (for demonstration purposes)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})



@app.teardown_appcontext
def close_db(error):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    """Main"""
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, thread=True)
