#!/usr/bin/python3
"""
Requirements:
- import app_views from api.v1.views
- create a route /status on the object app_views that returns a JSON:
"status": "OK" (see example)
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data
from models import storage
# Import classes for task 5
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def return_status():
    """Return status of GET request"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def return_stats():
    """
    Return the number of each object by type
    Se usa la funcion count() que creamos en la task 3, importamos storage
    ya que esta tiene creada las instancias de dbstorage y filestorage y asi
    podemos usar el metodo creado: count()
    """
    return jsonify({'amenities': storage.count(Amenity),
                    'cities': storage.count(City),
                    'places': storage.count(Place),
                    'reviews': storage.count(Review),
                    'states': storage.count(State),
                    'users': storage.count(User)})