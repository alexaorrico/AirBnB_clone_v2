#!/usr/bin/python3
"""
This is module 1-hbnb_route.
It starts a minimal Flask apllication.
Run it with python3 -m 1-hbnb_route or ./1-hbnb_route
"""
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_hbnb():
    """flask hello world"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """add a path to the url"""
    return "HBNB"


if __name__ == "__main__":
    # values here are the default, mentioned as keepsake
    app.run(host="0.0.0.0", port="5000")
