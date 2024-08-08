#!/usr/bin/python3
"""
Web flask application that displays the AirBnB clone webpage. Loads the
data from the database storage.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.place import Place
from models.amenity import Amenity


app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Display a page where the states, cities, places and amenities objects are
    loaded from the database storage.
    """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    return render_template('100-hbnb.html', states=states, amenities=amenities, places=places)

@app.teardown_appcontext
def remove_session(exception=None):
    """ Close storage session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 