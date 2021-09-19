#!usr/bin/python3
'''
Index file
'''


from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify

@app_views.route('/status', strict_slashes=False)
def appStatus():
    ''' Verifies status '''

    status = { "status": "OK" }
    return jsonify(status)
