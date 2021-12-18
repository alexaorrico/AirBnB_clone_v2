#!/usr/bin/python3
"""connecting to flask"""


from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def ap_te_do(self):
    """storage close"""
    storage.close()


@app.errorhandler(404)
def 404(e):
    """json 404"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host is None:
        host = "0.0.0.0"
    if port is None:
        port = "5000"
    app.run(host, port, threaded=True)
