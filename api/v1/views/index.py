#!/usr/bin/python3
'''creating an index route'''
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def return_status():
    return jsonify({"status": "200"})
