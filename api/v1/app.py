#!/usr/bin/python3
"""server configuration"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """cleanup operation at the end of a request"""
    storage.close()

@app.errorhandler(404)
def error_msg(error):
    """returns error 404 in JSON"""
    err = jsonify({"error": "Not found"})
    err.status_code = 404
    return err


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
