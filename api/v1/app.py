#!/usr/bin/python3
"""Task 4 Docstring"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """ Docstring for teardown """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ 404 error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    app.run(
        host=host,
        port=port,
        threaded=True,
        debug=True
    )
