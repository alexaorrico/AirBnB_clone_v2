#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 14:42:23 2020
@authors: Robinson Montes
          Mauricio Olarte
"""
from flask import Blueprint, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
    """Create a new view for State objects that handles all default
    RestFul API actions.
    """
    return jsonify([val.to_dict() for val in storage.all(State).values()])
