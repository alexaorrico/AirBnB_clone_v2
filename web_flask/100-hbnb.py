#!/usr/bin/python3
"""
    It will start a Flask web application.
    11. HBNB filters
"""

from flask import Flask, render_template
from models import *
from models import storage
import models

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """It displays a HTML page states, cities and Amenity and places listed"""
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    city = sorted(list(storage.all("cities").values()), key=lambda x: x.name)
    amenities = sorted(list(storage.all("Amenity").values()),
                       key=lambda x: x.name)
    return render_template('100-hbnb.html', states=states, city=city,
                           amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """It closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
