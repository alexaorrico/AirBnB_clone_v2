#!/usr/bin/python3
"""
flask app module
"""
from flask import Flask
import flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)


app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_app_context(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    '''Return this page when a 404 error appear'''
    data = {"error": "Not found"}
    return flask.jsonify(data), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
