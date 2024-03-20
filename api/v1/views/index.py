#!/usr/bin/python3
""" retruns json response status of API """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

app = Flask(__name__)

# Configure Flask to pretty-print JSON responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False


@app_views.route('/status')
def status():
    """ checks status of API """
    return jsonify({"status": "OK"})


@app_views.route('stats')
def get_number_objects():
    """ returns number of each object by types """
    classes = [Amenity, City, Place, Review, State, User]
    objects = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    number_objects = {
        objects[i]: storage.count(
            classes[i]) for i in range(
            len(classes))}
    return jsonify(number_objects)
