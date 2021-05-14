#!/usr/bin/python3
""" starts Flask app using db """

from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.amenity import Amenity
app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnbfilters():
        """ Displays dynamic filters """
        all_states = storage.all(State).values()
        all_amenities = storage.all(Amenity).values()
        return render_template(
                '10-hbnb_filters.html', states=all_states, amenities=all_amenities)


@app.teardown_appcontext
def teardown(self):
        """ Removes current session """
        storage.close()

if __name__ == "__main__":
        app.run(host='0.0.0.0', port='5000')
