#!/usr/bin/python3
"""Simple Flask web application"""
from flask import Flask
app = Flask('web_flask')


@app.route('/', strict_slashes=False)
def hello_route1():
    """Return 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hello_route2():
    """Return 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def hello_route3(text):
    """Return 'C ' followed by text from html request"""
    return 'C {}'.format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
