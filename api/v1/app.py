#!/usr/bin/python3
""" Flask Application main file """

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


HOST = os.environ.get('HBNB_API_HOST', '0.0.0.0')
PORT = os.environ.get('HBNB_API_PORT', '5000')


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_storage(exception):
    """ Close storage session """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ 404 Error handler """
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
