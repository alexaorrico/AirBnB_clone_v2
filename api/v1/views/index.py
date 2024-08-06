from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """  TODO: Doc """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """  TODO: Doc """
    res_dict = {}
    for key, value in classes.items():
        num_of_objs = storage.count(value)
        res_dict[key] = num_of_objs
    return jsonify(res_dict)
