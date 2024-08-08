#!/usr/bin/python3
"""
Script starts a Flask web application:
Routes:
 /states - list all states from storage
 /states/<id> -  list all cities in a specified state
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def delete_session(exception=None):
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def list_states_cities(id=None):
    """
    Displays a HTML page witha lists of all states if id=None or
    a list of cities of the specified states.
    """
    # Get list of states
    states = storage.all(State)
    state_key = None
    if id is not None:
        state_key = "State." + id
    return render_template('9-states.html', state_key=state_key, states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
