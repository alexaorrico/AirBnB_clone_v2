#!/usr/bin/python3
"""The flask app to initialise the api endpoint"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_storage(exception):
    storage.close()


if __name__ == "__main__":
    import os
    hbnb_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    hbnb_port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=hbnb_host, port=hbnb_port, threaded=True)
