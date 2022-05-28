#!/usr/bin/python3
"""
-------------------
New view for Cities
-------------------
"""
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from api.v1.views.aux_func import aux_func

methods = ["GET", "DELETE", "POST", "PUT"]
@app_views.route("/reviews/<review_id>", methods=methods)
def review_id(review_id):
    """
    -----------------
    Route for reviews
    -----------------
    """
    reviews = storage.all(Review)
    met = request.method
    if met in ["GET", "DELETE"]:
        res = aux_func(Review, met, review_id)
    elif met == "PUT":
        if review_id:
            key = "Review.{}".format(review_id)
            if key not in reviews.keys():
                abort(404)
            else:
                try:
                    data_review = request.get_json()
                    review = reviews[key]
                    for attr, value in data_review.items():
                        if attr not in ["id", "user_id", "place_id",
                                        "created_at", "updated_at"]:
                            setattr(review, attr, value)
                    # No sabemos si hay que guardar
                    storage.save()
                    return jsonify(review.to_dict()), 201, {'ContentType':
                                                            'application/json'}
                except Exception as err:
                    return jsonify("Not a JSON"), 400, {'ContentType':
                                                        'application/json'}
    return res


@app_views.route("/places/<place_id>/reviews", methods=methods)
def place_reviews(place_id=None):
    """
    ----------------------------------
    Retrieve a list of cities by state
    ----------------------------------
    """
    place_obj = storage.get(Place, place_id)
    if request.method == 'GET':
        if place_obj:
            reviews = [review.to_dict() for review in place_obj.reviews]
            return jsonify(reviews)
        else:
            abort(404)
    elif request.method == 'POST':
        if not place_obj:
            abort(404)
        data_review = request.get_json()
        if not data_review:
            return jsonify("Not a JSON"), 400, {'ContentType':
                                                'application/json'}
        elif "user_id" not in data_review.keys():
            return jsonify("Missing user_id"), 400, {'ContentType':
                                                     'application/json'}
        elif "text" not in data_review.keys():
            return jsonify("Missing text"), 400, {'ContentType':
                                                  'application/json'}
        elif storage.get(User, request.get_json()['user_id']) and place_obj:
            new_review = Review(**data_review)
            new_review.place_id = place_id
            # No sabemos si hay que guardar
            new_review.save()
            return jsonify(new_review.to_dict()), 201, {'ContentType':
                                                        'application/json'}
        else:
            abort(404)
