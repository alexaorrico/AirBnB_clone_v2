#!/usr/bin/python3
"""Definition of a Flask web application"""
from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route('/plenty/<int:times>')
def hello_world(times):
    return "Hello World\n" * times


if __name__ == "__main__":
    app.run(port=5000, debug=True)
