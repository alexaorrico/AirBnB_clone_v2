#!/usr/bin/python3
"""hello flask"""
from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    return "HBNB"


@app.route("/c/<text>")
def c_is(text):
    res = text.replace("_", " ")
    return f"C {res}"


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
