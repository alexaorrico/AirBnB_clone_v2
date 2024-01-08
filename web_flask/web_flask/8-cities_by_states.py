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


@app.route("/cities_by_states", strict_slashes=False)
def states_list():
    """A method to render an HTML page with a list of all State objects
    """
    states = storage.all(State).values()
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
