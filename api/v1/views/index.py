#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ Status ok """
    return jsonify({"status": "OK"})


if __name__ == '__main__':
    pass
