#!/usr/bin/python3
"""Flask Application"""
from models import storage
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)


CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(error):
    """404 page not found error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def close_db(error):
    """closes the storage"""
    storage.close()


if __name__ == "__main__":
    """Main Function"""
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
