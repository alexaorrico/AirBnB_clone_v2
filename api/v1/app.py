#!/usr/bin/python3
""" app.py """

from flask import Flask, make_reponse, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(self):
    """tear down app.py"""
    storage.close()


@auth.error_handler
def not_found():
    """ handles 404 errors"""
    return make_reposnse(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST") and os.getenv("HBNB_API_PORT"):
        app.run(host=os.getenv("HBNB_API_HOST"),
                port=os.getenv("HBNB_API_PORT"), threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
