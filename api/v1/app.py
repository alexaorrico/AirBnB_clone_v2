#!/usr/bin/python3
"""Flask App Engine"""
from flask import Flask, jsonify, make_response
import os
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exc):
    """Close storage"""

    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle error 404"""
    return make_response(jsonify({"error": "Not found"}))


if __name__ == "__main__":
    """Run App on loop"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
