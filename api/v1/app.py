#!/usr/bin/python3
""" first endpoint"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import make_response
from flask import jsonify
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_storage(self):
    """close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """close"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
