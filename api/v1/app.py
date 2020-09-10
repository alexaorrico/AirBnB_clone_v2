#!/usr/bin/python3
"""
Flask api app file
"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ close session """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ 404 not found """
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
