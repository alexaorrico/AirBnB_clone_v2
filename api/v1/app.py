#!/usr/bin/python3
"""
Magic right? (No need to have a pretty rendered output,
it’s a JSON, only the structure is important)
"""
import os
from flask import Flask
from flask import Blueprint
from flask import jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def hello(self):
    """Storage.close
    """
    storage.close()


@app.errorhandler(404)
def page_nf(e):
    """Error from page not found"""
    err_ = {
        "error": "Not found"
        }
    return jsonify(err_), 404


if __name__ == "__main__":
    """Host and Port
    """
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, debug=True, threaded=True)
