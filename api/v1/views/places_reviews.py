#!/usr/bin/python3
"""
Review model hold the endpoint (route) and their respective view functions
"""
from api.v1.views import (app_views, Review, storage)
from flask import (abort, jsonify, request)


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id):
    """Example endpoint returning a list of all reviews
    Retrieves a list of all reviews associated with a place
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        enum: ['279b355e-ff9a-4b85-8114-6db7ad2a4cd2']
        required: true
        default: '279b355e-ff9a-4b85-8114-6db7ad2a4cd2'
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the review
          place_id:
            type: string
            description: the id of the place
          text:
            type: string
            description: the text of the review
          updated_at:
            type: string
            description: The date the object was updated
          user_id:
            type: string
            description: The user id
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of dictionaries of all reviews objects
        schema:
          $ref: '#/definitions/State'
        examples:
            [{"__class__": "Review",
              "created_at": "2017-03-25T02:17:07",
              "id": "3f54d114-582d-4dab-8559-f0682dbf1fa6",
              "place_id": "279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
              "text": "Really nice place and really nice people. Secluded.",
              "updated_at": "2017-03-25T02:17:07",
              "user_id": "887dcd8d-d5ee-48de-9626-73ff4ea732fa"}]
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_json() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def one_review(review_id):
    """Example endpoint returning a list of one reivew
    Retrieves a list of one review associated with a place
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        enum: ["3f54d114-582d-4dab-8559-f0682dbf1fa6"]
        required: true
        default: "3f54d114-582d-4dab-8559-f0682dbf1fa6"
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the review
          place_id:
            type: string
            description: the id of the place
          text:
            type: string
            description: written review
          updated_at:
            type: string
            description: The date the object was updated
          user_id:
            type: string
            description: The user id
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of a dictionary of a Review objects
        schema:
          $ref: '#/definitions/State'
        examples:
            [{"__class__": "Review",
              "created_at": "2017-03-25T02:17:07",
              "id": "3f54d114-582d-4dab-8559-f0682dbf1fa6",
              "place_id": "279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
              "text": "Really nice place and really nice people. Secluded.",
              "updated_at": "2017-03-25T02:17:07",
              "user_id": "887dcd8d-d5ee-48de-9626-73ff4ea732fa"}]
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_one_review(review_id):
    """Example endpoint deleting one review
    Deletes a review based on the place_id
    ---
    definitions:
      Review:
        type: object
      Color:
        type: string
      items:
        $ref: '#/definitions/Color'

    responses:
      200:
        description: An empty dictionary
        schema:
          $ref: '#/definitions/City'
        examples:
            {}
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Example endpoint creates one review
    Creates one review associated with a place_id based on the JSON body
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        enum: ["3f54d114-582d-4dab-8559-f0682dbf1fa6"]
        required: true
        default: "3f54d114-582d-4dab-8559-f0682dbf1fa6"
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the review
          place_id:
            type: string
            description: the id of the place
          text:
            type: string
            description: written review
          updated_at:
            type: string
            description: The date the object was updated
          user_id:
            type: string
            description: The user id
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A list of a dictionary of a Review objects
        schema:
          $ref: '#/definitions/State'
        examples:
            [{"__class__": "Review",
              "created_at": "2017-03-25T02:17:07",
              "id": "3f54d114-582d-4dab-8559-f0682dbf1fa6",
              "place_id": "279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
              "text": "Really nice place and really nice people. Secluded.",
              "updated_at": "2017-03-25T02:17:07",
              "user_id": "887dcd8d-d5ee-48de-9626-73ff4ea732fa"}]
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if "user_id" not in r.keys():
        return "Missing user_id", 400
    if "text" not in r.keys():
        return "Missing text", 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    user = storage.get("User", r["user_id"])
    if user is None:
        abort(404)
    review = Review(**r)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_json()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Example endpoint creates one review
    Creates one review associated with a place_id based on the JSON body
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        enum: ["3f54d114-582d-4dab-8559-f0682dbf1fa6"]
        required: true
        default: "3f54d114-582d-4dab-8559-f0682dbf1fa6"
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          id:
            type: string
            description: the id of the review
          place_id:
            type: string
            description: the id of the place
          text:
            type: string
            description: written review
          updated_at:
            type: string
            description: The date the object was updated
          user_id:
            type: string
            description: The user id
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of a dictionary of a Review objects
        schema:
          $ref: '#/definitions/State'
        examples:
            [{"__class__": "Review",
              "created_at": "2017-03-25T02:17:07",
              "id": "3f54d114-582d-4dab-8559-f0682dbf1fa6",
              "place_id": "279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
              "text": "Really nice place and really nice people. Secluded.",
              "updated_at": "2017-03-25T02:17:07",
              "user_id": "887dcd8d-d5ee-48de-9626-73ff4ea732fa"}]
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    for k in ("id", "user_id", "place_id", "created_at", "updated_at"):
        r.pop(k, None)
    for key, value in r.items():
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_json()), 200
