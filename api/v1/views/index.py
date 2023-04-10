#!/usr/bin/python3
"""
import app_views from api.v1.views
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
from models import storage



app = Flask(__name__)

@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns the status of the application
    """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """
    Returns the number of objects by type
    """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    counts = []
    for key, val in classes.items():
        counts[key] = storage.count(val)
    return jsonify(counts), 200

if __name__ == '__main__':
    app.run(debug=True)
