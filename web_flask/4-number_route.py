#!/usr/bin/python3
"""
Module starts a Flask web applicatio and displays a 'Hello HBNBN'
message.
"""
from flask import Flask, abort


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_text(text):
    text = text.replace('_', ' ')
    return f"C {text}"


@app.route('/python/')
@app.route('/python/<text>', strict_slashes=False)
def default(text='is cool'):
    text = text.replace('_', ' ')
    return f"Python {text}"


@app.route('/number/<n>', strict_slashes=False)
def number(n):
    try:
        num = int(n)
        return f"{n} is a number"
    except ValueError:
        abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
