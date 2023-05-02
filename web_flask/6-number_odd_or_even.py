#!/usr/bin/python3
"""
    Sript that starts a Flask web application
 """
from flask import Flask, render_template
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


@app.route('/c/<text>', strict_slashes=False)
def text_var(text):
    """
        function to display text variable passed in
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python/<text>', strict_slashes=False)
def text_var_python(text="is cool"):
    """
        function to display text variable, with default "is cool"
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def var_num(n):
        """
             function to display a variable, but only if an int
        """
        return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def var_num_template(n):
        """
            function to display number in html page
        """
        return render_template("5-number.html", n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def var_num_even_odd(n):
        """
            function to display even or odd number
        """
        return render_template("6-number_odd_or_even.html", n=n)
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
