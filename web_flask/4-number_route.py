#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask, request
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Returns Hello HBNB! from 0.0.0.0:5000 """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Returns HBNB from 0.0.0.0:5000/hbnb """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """ Returns C followed by the value of text """
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is cool"):
    """ Returns Python followed by the vale of the text """
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """ Returns n is a number if n is an integer """
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
