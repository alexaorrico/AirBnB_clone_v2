#!/usr/bin/python3
"""index.py"""
from api.v1.views import app_views
from flask import Flask, jsonify


app = Flask(__name__)

@app_views.route("/status")
def status():
    json_text = jsonify({"status": "OK"})
    return json_text