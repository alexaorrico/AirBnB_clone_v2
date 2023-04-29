#!/usr/bin/python3

'''
Index file that renders the index.html template
'''

from flask import Flask, render_template, jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    '''Returns a JSON : "status": "OK"'''
    return jsonify(
            {
                "status": "OK"
            })
