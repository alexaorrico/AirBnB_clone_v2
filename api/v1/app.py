#!/usr/bin/python3
"""
Setup a Flask app

"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Tears down storage context"""
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
