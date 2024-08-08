#!/usr/bin/python3
"""
Web flask application displays a AirBnB web page with data of states,
cities and amenities loaded from the storage.

Route:
  /hbnb_filters - displays a HTML page like 6-index.html done on:
                  web_static repository
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Display a page where the states, cities and amenities objects are
    loaded from the database storage.
    """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template(
        '10-hbnb_filters.html', states=states, amenities=amenities)


@app.teardown_appcontext
def remove_session(exception=None):
    """ Close storage session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
