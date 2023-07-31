from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns status ok"""
    return jsonify({"status": "ok"})


@app_views.route('/api/v1/stats')
def count_objects():
    """retrieves all objects by classes"""
    stats = {}
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    for cls_name in classes:
        cls = storage.classes.get(cls_name)
        count = storage.count(cls)
        stats[cls_name.lower()] = count

    # Modify the keys to convert singular to plural
    for key, val in stats.items():
        if key.endswith('y'):
            stats[key[:-1] + 'ies'] = stats.pop(key)
        else:
            stats[key + 's'] = stats.pop(key)

    return jsonify(stats)
