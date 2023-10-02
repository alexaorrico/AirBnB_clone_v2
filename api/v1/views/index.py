#!/usr/bin/python3
from flask import Flask, jsonify
from . import app_views

app = Flask(__name__)

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def returnstuff():
    '''return stuff'''
    return jsonify(status='OK')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
