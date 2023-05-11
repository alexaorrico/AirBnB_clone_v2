from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status":"OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    statecount = storage.count(State)
    placecount = storage.count(Place)
    amenitycount = storage.count(Amenity)
    citycount = storage.count(City)
    reviewcount = storage.count(Review)
    usercount = storage.count(User)

    return jsonify({
        "amenities": amenitycount,
        "cities": citycount,
        "places": placecount,
        "reviews": reviewcount,
        "states": statecount,
        "users": usercount
    })