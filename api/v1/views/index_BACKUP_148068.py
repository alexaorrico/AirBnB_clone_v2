#!/usr/bin/python3
<<<<<<< HEAD
"""index"""
=======
"""Index page"""

>>>>>>> eb2505ce1a612d041181e43952ff196031b9062d
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = [Amenity, City, Place, Review, State, User]


@app_views.route('/status', strict_slashes=False)
def index_status():
    """Index route"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def get_stats():
<<<<<<< HEAD
=======
    """Get status"""
>>>>>>> eb2505ce1a612d041181e43952ff196031b9062d
    return jsonify(
        amenities=storage.count(Amenity),
        cities=storage.count(City),
        places=storage.count(Place),
        reviews=storage.count(Review),
        states=storage.count(State),
        users=storage.count(User)
            )
