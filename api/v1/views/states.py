#!/usr/bin/python3
from api.v1.app import app


@app.route('states', methods=['GET'])
def get_all_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "GET ITEMS"

@app.route('states/<state_id>', methods=['GET'])
def get_all_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "GET ITEM"

@app.route('states', methods=['POST'])
def post_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "POST ITEM"

@app.route('states/<state_id>', methods=['DELETE'])
def delete_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "DELETE ITEM"

@app.route('states/<state_id>', methods=['PUT'])
def get_all_state():
    """returns HOW MANY DATA IN STORAGE"""
    return "UPDATE ITEM"