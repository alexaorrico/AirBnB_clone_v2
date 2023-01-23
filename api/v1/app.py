#!/usr/bin/python3
"""flask setup"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(exc):
    """teardown method"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """404 error"""
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)
