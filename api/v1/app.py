#!/usr/bin/python3
"""flask application"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint, make_response
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """ this for slash routing"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a JSON-formatted 404 status code"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', 5000)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT,
            threaded=True)
