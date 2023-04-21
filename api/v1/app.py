#!/usr/bin/python3
"""
Flask app module.
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root_path():
    """
    GET /
    """
    return jsonify({'message': 'Hello World'})


if __name__ == '__main__':
    app.run()
