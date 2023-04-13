#!/usr/bin/python3
from api.v1.app import app
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'])
def get_all_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "GET ITEMS"

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "GET ITEM"

@app_views.route('/states', methods=['POST'])
def post_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "POST ITEM"

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "DELETE ITEM"

@app_views.route('states/<state_id>', methods=['PUT'])
def update_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "UPDATE ITEM"