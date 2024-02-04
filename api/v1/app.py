#!/usr/bin/python3
"""
creates a variable app, instance of Flask
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the database again at the end of the request."""
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """returns 'Not found'"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
