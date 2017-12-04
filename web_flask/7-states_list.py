#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def states_list():
    """display a HTML page with the states listed in alphabetical order"""
    states = storage.all("State").values().sort(key=lambda x: x.name)
    return render_templace('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')
