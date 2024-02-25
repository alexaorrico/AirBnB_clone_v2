#!/usr/bin/python3
"""
Route for handling review objects and operations.
"""
from flask import justify, abort, request
from flask import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
  """
  Retrieves all review objects by place
  :return: json of all reviews
  """
  review_list = []
  place_obj = storage.get("Place", str(place_id))

  if place_obj is None:
    abort(404)

  for obj in place_obj.reviews:
    review_list.append(obj.to_json())

  return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def reviews_create(place_id):
    """
  Creates the reviews route
  :return: created review obj
  """
  review_json = request.get_json(silent=True)
  if review_json is None:
    abort(400, 'Not a JSON')
  if not storage.get("Place", place_id):
    abort(404)
  if not storage.get("User", review_json["user_id"]):
    abort(404)
  if "user_id" not in review_json:
    abort(400, 'Missing user_id')
  if "text" not in review_json:
    abort(400, 'Missing text')

  review_json["place_id"] = place_id

  new_review = Review(**review_json)
  new_review.save()
  resp = jsonify(new_review.to_json())
  resp.status_code = 201

  return resp


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
  """
  Gets a specific review obj by id
  :param review_id: place obj id
  :return: review obj with specified id or error
  """

  fetched_obj = storage.get("Review", str(review_id))

  if fetched_obj is None:
    abort(404)

  return jsonify(fetched_obj.to_json())


@app_views.route("/places/<place_id>/reviews", methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
  """
  Update specific review obj by id
  :param review_id: review obj id
  :return: review object and 200 on success, or 400 or 404 on failure
  """
  place_json = request.get_json(silent=True)

  if place_json is None:
    abort(400, 'Not a JSON')

  fetched_obj = storage.get("Review", str(review_id))

  if fetched_obj is None:
    abort(404)

  for key, val in place_obj.items():
    if key not in ["id", "created_at", "updated_at", "user_id",
                   "place_id"]:
        setattr(fetched_obj, key, val)

  fetched_obj.save()

  return jsonify(fetched_obj.to_json())


@app_views.route("/places/<place_id>/reviews", methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
  """
  Delete review by id
  :param: review obj id
  :return: empty dict with 200 or 404 if not found
  """

 fetched_obj = storage.get("Review", str(review_id))

  if fetched_obj is None:
    abort(404)

  storage.delete(fetched_obj)
  storage.save()

  return jsonify({})
