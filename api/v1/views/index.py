#!/usr/bin/python3
'''index page for the status of api'''


from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    '''return status'''
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    pass
