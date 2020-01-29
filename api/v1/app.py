#!/usr/bin/python3
""" first endpoint"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import make_response
from flask import jsonify
import os


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_storage(e):
    """close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """close"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=os.environ.get("HBNB_API_HOST", "0.0.0.0"),
            port=os.environ.get("HBNB_API_PORT", "5000"), threaded=True)
