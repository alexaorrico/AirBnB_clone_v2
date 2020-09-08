#!/usr/bin/python3
"""comment"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.review import Review
from models.place import Place


@app_views.route('/api/v1/places/<place_id>/reviews')
def get_reviews():
    """yelp"""
    lizt = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place_id:
            lizt.append(review.to_dict())
    return jsonify(lizt)


@app_views.route('/api/v1/reviews/<review_id>')
def get_a_review():
    """review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
