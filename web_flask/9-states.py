#!/usr/bin/python3
"""Flask Web App that returns list of states"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """teardown_db closes connections to database"""
    if storage is not None:
        storage.close()


# def state_list():
#     """get all state info from database"""
#     states = storage.all(State)
#     return render_template("9-states.html", states=states)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_city(id=None):
    """get all state info from database"""
    states = storage.all(State)
    for state in states.values():
        if id and state.id == id:
            return render_template("9-states.html", id_state=state)
    state = states.values()
    return render_template("9-states.html", states=state)


@app.route("/cities_by_states", strict_slashes=False)
def city_list():
    """get all state and city info from database"""
    states = storage.all(State)
    return render_template("9-states.html", states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
