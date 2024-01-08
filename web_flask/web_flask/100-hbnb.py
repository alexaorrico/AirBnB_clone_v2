#!/usr/bin/python3
"""A python script that starts a Flask web app listening on 0.0.0.0, port 5000
"""
from ctypes.wintypes import PLARGE_INTEGER
from models import storage
from flask import Flask, render_template
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """A method to remove the current SQLAlchemy Session
    """
    storage.close()
    
@app.route('/hbnb', strict_slashes=False)
def hbnb_filter():
    """display a HTML page
    """
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    
    states = sorted(states, key=lambda state: state.name)
    for state in states:
        state.cities = sorted(state.cities, key=lambda city: city.name)
    cities = sorted(cities, key=lambda city: city.name)
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    places = sorted(places, key=lambda place: place.name)
    
    
    
    return render_template('100-hbnb.html', states=states, amenities=amenities, places=places)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    