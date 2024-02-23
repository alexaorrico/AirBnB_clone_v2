#!/usr/bin/python3
"""
api flask app
"""
from flask import Flask, jsonify
import models
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')


@app.teardown_appcontext
def close_db(self):
    """text"""
    storage.close()

@app.errorhandler(404)
def not_found_error(error):
    """error handler function"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    if HBNB_API_HOST and HBNB_API_PORT:
        app.run(host=HBNB_API_HOST, port=HBNB_API_PORT,
                debug=True, threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000,
                debug=True, threaded=True)
