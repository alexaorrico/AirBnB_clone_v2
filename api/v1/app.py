#!/usr/bin/python3
"""RESTful API module"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.register_blueprint(app_views, url_prefix="/api/v1")
    app.run(host='0.0.0.0', port=5000, threaded=True)
