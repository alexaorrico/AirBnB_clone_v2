#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template, url_for
import uuid
app = Flask(__name__)
app.url_map.strict_slashes = False
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/101-hbnb/')
def hbnb(an_id=None):
    """ HBNB is alive! """
    state_obj = storage.all(State).values()
    states = dict([state.name, state] for state in state_obj)
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())
    cache_id = uuid.uuid4()
    c_id = (str(cache_id))
    return render_template('101-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places,
                           users=users,
                           cache_id=c_id)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)
    
