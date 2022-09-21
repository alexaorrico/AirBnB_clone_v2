#!/usr/bin/python3
"""module for flask application """
import os
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDownDB(self):
    """removes sqlalchemy session"""
    storage.close()


@app.errorhandler(404)
def errorHandler(error):
    """returns a 404 error msg"""
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST') or '0.0.0.0',
            port=os.getenv('HBNB_API_PORT') or '5000',
            threaded=True)
