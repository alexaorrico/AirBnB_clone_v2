#!/usr/bin/python3
"""
Status of my API
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
import os
app = Flask(__name__)


app.register_blueprint(app_views)
@app.teardown_appcontext
def tear(error):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
