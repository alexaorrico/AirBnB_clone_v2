#!/usr/bin/python3
""" Handle RESTful API request for states"""


from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def all_review(place_id):
    """ GET ALL reviews """

    # search if place_id exist, if not return 404
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    # list all reviews linked to the place
    review_list = place.reviews
    # make a list with all diccionaries of reviews
    review_dict = []
    for review in review_list:
        review_dict.append(review.to_dict())
    # return the list with the data
    return jsonify(review_dict)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a specific review """
    # load review_id instance if not exists abort 404
    instance = storage.get(Review, review_id)
    if not instance:
        abort(404)
    return jsonify(instance.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a review"""
    # load the review and deletes if not exists returns 404
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
    """Creates a create_review """

    # validate type of request if invalid return 400
    if not request.get_json():
        abort(400, description="Not a JSON")

    # load place_id if not exists return 404
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    # load json  request as dict
    data = request.get_json()
    # update data dict with place_id
    data['place_id'] = place_id

    # validate minimal attributes for instance creation
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'user_id'not in data:
        abort(400, description="Missing user_id")
    if 'text' not in data:
        abort(400, description="Missing text")

    # validate if user_id exists
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    # create a new instance
    new_instance = Review(**data)

    # saves new_instance
    new_instance.save()

    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_revie(review_id):
    """update a State: POST /api/v1/states"""

    # validate type of request if invalid return 400
    if not request.get_json():
        abort(400, description="Not a JSON")

    # loads request ti dict
    data = request.get_json()

    # load the review_id if not exists returns 404
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    # fields that can not be update
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    # update the instance with the data
    for key, value in data.items():
        if key not in ignore:
            setattr(obj, key, value)
    # saves updated obj
    obj.save()

    return make_response(jsonify(obj.to_dict()), 200)
