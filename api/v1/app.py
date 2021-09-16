#!/usr/bin/python3
""" Flask app with cors module   """

from models import storage
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

if __name__ == "__main__":
    """ Flask main function """
    app.run(debug=True)
