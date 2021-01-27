#!/usr/bin/python3
"""Run a Flask web application"""


from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardonwn_db(exception):
    """Method to call 'storage.close()'"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """error 404: Not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
