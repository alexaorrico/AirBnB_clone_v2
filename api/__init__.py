#!/usr/bin/python3
"""
APP
"""
from flask import jsonify as _jsonify


def jsonify(*args, status=200):
    """create a json response"""
    response = _jsonify(*args)
    response.status_code = status
    return response
