#!/usr/bin/python3


"""  TODO: Doc """


from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """  TODO: Doc """
    array_of_objs = []
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404, description="State not found")
    else:
        for value in place_obj.reviews:
            array_of_objs.append(value.to_dict())
        return jsonify(array_of_objs)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews_ById(review_id):
    """  TODO: Doc """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404, description="Review not found")
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(review_id):
    """  TODO: Doc """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404, description="Review not found")
    try:
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500, description="Error while deleting")


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_city(place_id):
    """  TODO: Doc """
    if request.is_json:
        data = request.get_json()
        if 'text' not in data:
            abort(400, description="Missing text")
        elif 'user_id' not in data:
            abort(400, description="Missing user_id")
        else:
            place_obj = storage.get(Place, place_id)
            if not place_obj:
                abort(404, description="State not found")
            review_obj = Review(**data)  # unpack dict as key:valus
            review_obj.place_id = place_obj.id
            review_obj.save()
            return jsonify(review_obj.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_city(review_id):
    """  TODO: Doc """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404, description="State not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    bad_keys = ['id', 'place_id', 'user_id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in bad_keys:
            setattr(review_obj, key, data[key])
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
