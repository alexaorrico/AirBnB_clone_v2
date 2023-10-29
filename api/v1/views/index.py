from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def check_status():
    """
    returns the status
    """
    if request.method == "GET":
        response = {"status": "OK"}
        return jsonify(response)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    retrieves the number of each objects by type
    """
    response = {}
    for key, value in classes.items():
        response[key] = storage.count(value)
    return jsonify(response)
