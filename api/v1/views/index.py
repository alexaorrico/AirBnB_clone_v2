#!/usr/bin/python3
""" Api """

from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)
@app_views.route('api/v1/status')

def return_jason():
    """ return json status"""
    return jsonify(status = 'OK')
