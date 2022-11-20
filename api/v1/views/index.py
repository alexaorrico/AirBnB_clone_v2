#!/usr/bin/python3
""" Creates the index file """
from flask import jsonify
from api.v1.views import app_views

@app.views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of blueprint API ""
    return jsonify({status: "OK"})
