#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask, request, render_template

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
def c_with_text(text):
    """ Returns C followed by the value of text """
    formatted_text = text.replace('_', ' ')
    return "C {}".format(formatted_text)


@app.route('/python', defaults={'text', 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_with_text(text):
    """ Returns Python followed by the vale of the text """
    formatted_text = text.replace('_', ' ')
    return "Python {}".format(formatted_text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ Returns n is a number if n is an integer """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ Returns an HTML page only if n is an integer """
    return render_template("5-number.html", n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_old_or_even(n):
    """ Returns an HTML page only if the n is an integer """
    # Check if n is an integer
    if isinstance(n, int):
    # Determine if n is even or odd
        even_or_odd = 'even' if n % 2 == 0 else 'odd'
    # Render the template and pass the
    # value of n and even_or_odd to the template
        return render_template("6-number_odd_or_even.html", n=n, even_or_odd=even_or_odd)
    else:
    # If n is not an interger, return an error message
        return 'Invalid input. Please provide an integer.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
