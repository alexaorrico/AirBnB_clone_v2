#!/usr/bin/python3
"""Index file"""

from api.v1.views import app_views
from flask import Flask, jsonify
# from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app_views.route('/status')
def index():
    return jsonify({'status': 'OK'})
