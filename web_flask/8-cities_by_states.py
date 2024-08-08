#!/usr/bin/python3
"""
Script starts a Flask web application:
Requirements:
 - Routes:
      /states_list: display a HTML page: (inside the tag BODY)
      H1 tag: “States”
      UL tag: with the list of all State objects present in DBStorage
      sorted by name (A->Z) tip
         LI tag: description of one State: <state.id>: <B><state.name></B>
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def delete_session(exception=None):
    """ Closes the current session after each request """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def list_cities_states():
    """ Displays a HTML that contains a list of all State objects """
    # Get records of the states
    states = storage.all(State).values()
    return render_template(
        '8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
