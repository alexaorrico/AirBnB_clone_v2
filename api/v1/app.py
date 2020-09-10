#!/usr/bin/python3
"""API Module"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Method Handle"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Error 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True, debug=True)
