#!/usr/bin/python3
"""Flask Setup"""

from models import storage
from api.v1.views import app_views
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close():
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
