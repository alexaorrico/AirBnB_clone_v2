#!/usr/bin/python3
""" Starts a Flask Web Application """

from flask import Flask, render_template
import uuid
from models import storage
from models.amenity import Amenity


app = Flask(__name__)


@app.route('/1-hbnb', strict_slashes=False)
def hbnb():
    """ Render Template """
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    return render_template('1-hbnb.html', amenities=amenities, cache_id=str(uuid.uuid4()))


if __name__ == "__main__":
    """ Run port """
    app.run(host='0.0.0.0', port=5001)