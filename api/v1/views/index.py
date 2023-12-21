"""Index view for api v1"""

# Import necessary modules and classes
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Define route to return JSON status
@app_views.route("/status")
def status():
    """Returns status of API"""
    # Return a JSON response with the status
    return jsonify({"status": "OK"})

# Define route to return JSON stats
@app_views.route("/stats")
def stats():
    """Retrieves number of each objects by type"""
    # Define a dictionary with the classes to count
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    # Return a JSON response with the count of each class
    return jsonify({key: storage.count(value) for key, value in classes.items()})