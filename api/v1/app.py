#!/usr/bin/python3
"""flask"""
from flask import Flask, render_template, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_db(self):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """404ed"""
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
