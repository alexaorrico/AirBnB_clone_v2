#!/usr/bin/python3
""" returns json statuses for app_views routes  """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def stat_return():
    """ return json status: OK """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat_count():
    """ endpoint that retrieves the # of each objects by type """
    count_stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(count_stats)


if __name__ == "__main__":
    pass
