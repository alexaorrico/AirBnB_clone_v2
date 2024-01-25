#!/usr/bin/python3
'''A minimal Flask Application'''
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    '''home'''
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(debug=True)
