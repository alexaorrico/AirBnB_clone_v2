#!/usr/bin/python3
"""restful actions for users"""
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route('/api/v1/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def get_all_reviews(id):
    """gets all reviews of a place"""
    review_list = []
    get_place = storage.get(Place, id)
    if get_place is None:
        abort(404)
    else:
        for review in get_place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)


@app_views.route('/api/v1/reviews/<review_id>', methods=["GET"],
                 strict_slashes=False)
def get_review(id):
    """retrieves a review by id"""
    get_review = storage.get(Review, id)
    if get_review is None:
        abort(404)
    else:
        return jsonify(get_review.to_dict())


@app_views.route('/api/v1/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def del_review(id):
    """deletes a review by id"""
    empty_dict = {}
    get_review = storage.get(Review, id)
    if get_review is None:
        abort(404)
    else:
        storage.delete(get_review)
        storage.save()
        return empty_dict, 200


@app_views.route('/api/v1/places/<place_id>/reviews', methods["POST"],
                 strict_slashes=False)
def create_review(id):
    """creates a review object from place id"""
    review_json = request.get()
    get_place = storage.get(Place, id)
    if get_place is None:
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    elif 'user_id' not in review_json:
        abort(400, description="Missing user_id")
    elif 'text' not in review_json:
        abort(400, description="Missing text")
    else:

        ###########################################
        ###########################################
        # how to actually create new review object? #
        ###########################################
        ###########################################
        return


@app_view.route('/api/v1/reviews/<review_id>', methods=["PUT"],
                strict_slashes=False)
def update_review(id):
    """updates a review object"""
    review_json = request.get_json
    get_place = storage.get(Place, id)
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if get_place is None:
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    else:
        for key, value in review_json.items:
            if key not in ignored_keys:
                setattr(get_place, key, value)
            storage.save()
        return jsonify(get_place.to_dict()), 201
