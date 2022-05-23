#!/usr/bin/python3
"""
    state
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import requests
from os import *


@app.views.route("/states", methods=['GET'])
def get_states():
    """
        comment
    """
    states = storage.all("State").values()
    return jsonify([state.to_json() for state in states])
