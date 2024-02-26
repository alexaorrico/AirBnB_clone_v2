from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Retrieves the number of each object by type.
    """
    stats = {}
    classes = ["User", "State", "City", "Amenity", "Place", "Review"]

    for cls_name in classes:
        cls_count = storage.count(cls_name)
        stats[cls_name] = cls_count

    return jsonify(stats)
