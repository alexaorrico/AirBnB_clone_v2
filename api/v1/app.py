#!/usr/bin/python3
"""run script"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception):
    "Close the session after each request"
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handle 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


if __name__ == "__main__":
    """run the app"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
