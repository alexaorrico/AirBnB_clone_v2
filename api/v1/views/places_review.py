#!/usr/bin/python3
""" Handle RESTful API request for states"""


from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def all_places(place_id):
    """ GET ALL PLACES """
    place = storage.all(Place).values()
    if not place:
        abort(404)
    review_list = place.reviews
    review_dict = []
    for review in review_list:
        review_dict.append(review.to_dict())

    return jsonify(review_dict)

@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a specific user """
    instance = storage.get(Review, review_id)
    if not instance:
        abort(404)
    return jsonify(instance.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    obj = storage.get(Review, review_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a amenity """

    if not request.get_json():
        abort(400, description="Not a JSON")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    data['place_id'] = place_id

    if not 'name' in data:
        abort(400, description="Missing name")
    if not 'user_id' in data:
        abort(400, description="Missing user_id")
    if not 'text' in data:
        abort(400, description="Missing text")
        
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    new_instance = Review(**data)
    new_instance.save()

    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_revie(review_id):
    """update a State: POST /api/v1/states"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    obj = storage.get(Review, review_id)

    if not obj:
        abort(404)

    data = request.get_json()

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(obj, key, value)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 200)
