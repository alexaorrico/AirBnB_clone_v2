#!/usr/bin/python3
"""
This file is the main entry point
for the AirBnB clone version 3 API.
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify

app = Flask('__name__')
app.register_blueprint(app_views)


@app.errorhandler(404)
def notFound(err):
    return make_response(jsonify({"statue": " Not Found 404"}), err)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
