#!/bin/bash/python3
"""
This is flask app that integrates with airbnbn static html template.
"""
from flask import Flask, render_template, url_for
from models import storage
import uuid


# setup for flask
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


# start rendering flask page
@app.teardown_appcontext
def teardown_db(exception):
    """
    this method calls .close() on the current SQLAlchemy session after each request
    """
    storage.close()


@app.route('/0-hbnb')
def hbnb_filters(the_id=None):
    """
    handle requests to custom template with, cities and amenities
    """
    state_objs = storage.all('State').values()
    states = dict([state.name, state] for state in state_objs)
    amens = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
            for user in storage.all('User').values())
    return render_template('0-hbnb.html', 
            states=states, 
            amens=amens, 
            places=places, 
            users=users, 
            cache_id=uuid.uuid4())

if __name__ == "__main__":
    """
    Main flask app
    """
    app.run(host=host, port=port)
