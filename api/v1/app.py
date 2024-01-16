#!/usr/bin/python3
"""app.py file"""
from flask import Flask, Blueprint, render_template
from flask import jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exception):
    """calls close()"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') is None:
        host = '0.0.0.0'
    else:
        host = getenv('HBNB_API_HOST')

    if getenv('HBNB_API_PORT') is None:
        port = 5000
    else:
        port = getenv('HBNB_API_PORT')
    app.run(host=host, port=port)
