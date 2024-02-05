#!/usr/bin/python3
"""
Runs a Flask web application on 0.0.0.0:5000
"""
from models import storage
from flask import Flask, render_template
from models.state import State
from sqlalchemy.orm import scoped_session, sessionmaker

#creates an instance of the Flask class and assigns it to the variable app
app = Flask(__name__)


# Teardown app context to remove the
# current SQLAlchemy session after each request
@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session"""
    storage.clone()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Returns an HTML page of all States sorted by name"""
    states = sorted(storage.all(State).value(), key=lambda s: s.name)
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    """Run on 0.0.0.0"""
    app.run(host='0.0.0.0', port=5000)
