#!/usr/bin/python3
""" Starts a Flash Web Application """


from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid


app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ Close SQLAlchemy Session """
    storage.close()


@app.route('/0-hbnb', strict_slashes=False)
def hbnb():
    """ Render Template """

    return render_template('0-hbnb.html', cache_id=str(uuid.uuid4()))


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)