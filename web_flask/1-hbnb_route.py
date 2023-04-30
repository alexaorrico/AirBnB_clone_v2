#!/usr/bin/python3
"""
    Sript that starts a Flask web application
 """
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbn():
    """
        function to return Hello HBNB!
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
        function to return HBNB
    """
    return "HBNB"
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
