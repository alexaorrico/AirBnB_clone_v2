#!/usr/bin/python3
"""a script to return the status of the API"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.register_blueprint(app_views)
@app.teardown_appcontext
def session_close(exception):
    """close session"""
    storage.close()

@app.errorhandler(404)
def handle_404(exep):
    """error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
