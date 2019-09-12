#!/usr/bin/python3
""" API class """
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def _handle_api_error(ex):
    """  handle error 404 """
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST') or '0.0.0.0',
            port=getenv('HBNB_API_PORT') or 5000, threaded=True)
