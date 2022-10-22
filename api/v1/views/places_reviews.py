from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by(place_id):
    place = storage.get(Place, place_id)
    review_dict = []
    for review in place.reviews:
            review_dict.append(review.to_dict())
    return jsonify(review_dict)

@app_views.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    try:
        review = storage.get(Review, review_id)
        return jsonify(review.to_dict())
    except KeyError:
        abort(404)

@app_views.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    try:
        review = storage.get(Review, review_id)
        review.delete()
        storage.save()
        return jsonify({})
    except KeyError:
        abort(404)

@app_views.route('/places/<string:place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    try:
        place = storage.get(Place, place_id)
        data = request.get_json()
        if data.get("name") is None:
            return make_response(jsonify({"error" : "Missing name"}), 400)
        if data.get("user_id") is None:
            return make_response(jsonify({"error" : "Missing user_id"}), 400)
        data["place_id"] = place_id
        review = Review(**data)
        review.save()
        response = jsonify(review.to_dict())
        return make_response(response, 201)
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error" : "Not a JSON"}), 400)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    try:
        data = request.get_json()
        review = storage.get(Review, review_id)
        for key, value in data.items():
            if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                continue
            setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error" : "Not a JSON"}), 400)
