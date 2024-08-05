#!/usr/bin/python3
"""Create Flask app for API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy Session"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 error response"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
