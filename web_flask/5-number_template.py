#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_holberton():
    """Returns a string at the root route"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns a string at the /hbnb route"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    """Returns a string at the /c/<text> route,
    expands the <text> variable"""
    new = text.replace('_', ' ')
    return 'C %s' % new


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pythoniscool(text):
    """Returns a string at the /python route, with a default text
    of 'is cool', or the expansion of <text>"""
    new = text.replace('_', ' ')
    return 'Python %s' % new


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Returns a string at the /number/<n> route,
    only if n is an int"""
    if type(n) == int:
        return '%i is a number' % n


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Returns a template at the /number_template/<n> route,
    expanding route"""
    if type(n) == int:
        return render_template('5-number.html', n=n)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
