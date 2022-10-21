#!/usr/bin/python3
"""This program will retrieve state object with json format"""
from flask import Flask, make_response, request, jsonify
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    resp_json = []
    all_states = list(storage.all('State'))
    resp_json = [BaseModel(state).to_dict() for state in all_states]
    return jsonify(resp_json)

