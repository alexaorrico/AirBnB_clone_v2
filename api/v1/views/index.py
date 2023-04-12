#!/usr/bin/python3

from api.v1.app import app

@app.route('/status', strict_slashes=False)
def index():
    """returns STATUS OK"""
    return '{"status": "OK"}'


@app.route('/stats', strict_slashes=False)
def count():
    """returns HOW MANY DATA IN STORAGE"""
    return '{"status": "OK"}'
