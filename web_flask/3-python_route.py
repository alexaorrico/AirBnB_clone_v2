#!/usr/bin/python3
"""
This is module 3-python_route.
It starts a minimal Flask apllication.
Run it with python3 -m 3-python_route or ./3-python_route
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


@app.route('/c/<text>')
def c_text(text):
    """make a simple variable rule"""
    return "C {}".format(text.replace("_", " "))


@app.route('/python/')   # , defaults={'text': "is cool"})
# redirection, strict_slashes prevents the 301 redirect when missing last /
# see http://stackoverflow.com/a/17628419/7484498
# the default value can be put in 2 different places.
@app.route('/python/<text>')
def python_text(text="is cool"):
    """give a rule a default value"""
    return "Python {}".format(text.replace("_", " "))


if __name__ == "__main__":
    # values here are the default, mentioned as keepsake
    app.run(host="0.0.0.0", port="5000")
