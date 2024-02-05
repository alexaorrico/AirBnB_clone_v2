from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    Amenity: 'amenities',
    City: 'cities',
    Place: 'places',
    Review: 'reviews',
    State: 'states',
    User: 'users'
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    dict = {}
    for key, value in classes.items():
        dict[value] = storage.count(key)
    return jsonify(dict)

