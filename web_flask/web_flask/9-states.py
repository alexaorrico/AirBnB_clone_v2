#!/usr/bin/python3
"""A python script that starts a Flask web app listening on 0.0.0.0, port 5000
"""
from models import storage
from flask import Flask, render_template
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """A method to remove the current SQLAlchemy Session
    """
    storage.close()


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_id(id=None):
    """A method to render an HTML page with a list of all State objects
    """
    states = storage.all(State).values()
    if id:
        states = [state for state in states if state.id == id]
    states = sorted(states, key=lambda state: state.name)
    for state in states:
        state.cities = sorted(state.cities, key=lambda city: city.name)
    return render_template("9-states.html", states=states, id=id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
