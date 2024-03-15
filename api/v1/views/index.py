#!/bin/usr/python3
""" retruns json response status of API """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ checks status of API """
    return jsonify({"status":"OK"})


if __name__ == '__main__':
    app_views.run(debug=True, host='0.0.0.0', port='5000')
