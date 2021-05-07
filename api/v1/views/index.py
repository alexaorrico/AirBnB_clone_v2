#!/usr/bin/python3

from flask import Flask
from flask.json import jsonify

from api.v1.views import app_views

app = Flask(__name__)

@app.route('/status')
def app_views():
    return jsonify({"status": "OK"})
