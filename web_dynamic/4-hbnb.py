#!/usr/bin/python3
""" Starts a Flask Web Application """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template, request
import uuid

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@app.route('/4-hbnb/', strict_slashes=False)
def hbnb():
    """ HBNB is alive! """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    cache_id = str(uuid.uuid4())

    return render_template('4-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           cache_id=cache_id)

@app.route('/4-hbnb/filter', methods=['POST'], strict_slashes=False)
def filter_hbnb():
    """ Handle filtering of places based on selected amenities """
    amenity_ids = request.get_json().get('amenities')
    
    if not amenity_ids:
        amenity_ids = []
    
    filtered_places = []
    places = storage.all(Place).values()

    for place in places:
        if all(amenity_id in place.amenity_ids for amenity_id in amenity_ids):
            filtered_places.append(place)

    return render_template('4-hbnb.html',
                           filtered_places=filtered_places)

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
