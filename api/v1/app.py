#!/usr/bin/python3
"""
starts a Flask web application
"""
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv

host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ 404 handler """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000
    app.run(host='0.0.0.0', port=5000, threaded=True)
