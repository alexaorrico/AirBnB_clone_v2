#!/usr/bin/python3
"""
Status of your API
"""

from os import getenv
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(self):
    """
    Calls storage.close()
    """

    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    404 error
    """
    dic_error = {"error": "Not found"}
    return make_response(jsonify(dic_error), 404)


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', '5000')
    app.run(host=HOST, port=PORT, threaded=True)
