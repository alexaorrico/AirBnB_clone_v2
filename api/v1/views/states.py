#!/usr/bin/python3
"""view for state  that handles all default RESTFul API actions"""
from api.v1.views import app_views
# from api.v1 import app
from flask import Flask, jsonify
from models import storage


@app_views.route("/states/", methods=["GET"])
def get_all_states():
    """get all state"""
    states = [obj.to_dict() for obj in storage.all("state")]
    return states

# @app_views.route("/states/<state_id>", methods=["GET"])
# def get_state_by_Id(state_id):
#     """get state by id"""
#     try:
#         return storage.get("State", state_id)
#     except:
#         return error_handler(e)
