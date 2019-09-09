from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def json_string():
    new = {}
    new['status'] = "OK"
    return jsonify(new)


@app_views.route('/stats')
def obj_by_count():
    new = {}
    cls_list = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    for i in cls_list:
        new[i] = storage.count(i)
    return jsonify(new)
