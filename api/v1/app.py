#!/usr/bin/python3
"""app.py"""
from flask import Flask, Blueprint, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """return a 404 error as a JSON response"""
    return {"error": "Not found"}, 404

@app.teardown_appcontext
def terminate(exc):
    """Close SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
