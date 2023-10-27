#!/usr/bin/python3
"""
This is the module for our flask app
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return jsonify(error='Not found'), 404


@app.teardown_appcontext
def close_session(exe):
    """This close the sqlAlchemy session"""
    return storage.close


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
