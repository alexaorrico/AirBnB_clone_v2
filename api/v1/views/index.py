from flask import jsonify
from api.v1.views import app_views
from models import storage

#return api status code
@app_views.route("/status", methods=["GET"])
def status():
    #api status code
    return jsonify({"status": "OK"})


#retrieve number of each object type 
@app_views.route("/stats", methods=["GET"])
def stats():
    """Retrieve the number of each object type"""
    stats_dict = {}
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]

    for cls_name in classes:
        cls = storage.get(cls_name)
        if cls:
            stats_dict[cls_name] = storage.count(cls)

    return jsonify(stats_dict)
