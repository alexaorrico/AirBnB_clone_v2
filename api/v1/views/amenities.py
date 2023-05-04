#!/usr/bin/python3
"""
This is module amenities
"""
from api.v1.views import (app_views, Amenity, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def view_amenity(amenity_id=None):
    """Example endpoint returning a list of all amenities or of one specified
    Retrieves a list of all amenties or of one specified by amenity_id
    ---
    parameters:
      - name: amenity_id
        in: path
        type: string
        enum: ["all", cf701d1a-3c19-4bac-bd99-15321f1140f2", None]
        required: true
        default: None

    definitions:

      Amenity:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          email:
            type: string
          first_name:
            type: string
          last_name:
            type: string
          id:
            type: string
            description: the id of the user
          updated_at:
            type: string
            description: The date the object was updated
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of dicts or dict, each dict is an amenity
        schema:
          $ref: '#/definitions/Amenity'
        examples:
            [{"__class__": "Amenity",
              "created_at": "2017-03-25T02:17:06",
              "id": "cf701d1a-3c19-4bac-bd99-15321f1140f2",
              "name": "Dog(s)",
              "updated_at": "2017-03-25T02:17:06"}]
    """
    if amenity_id is None:
        all_amenities = [state.to_json() for state
                         in storage.all("Amenity").values()]
        return jsonify(all_amenities)
    s = storage.get("Amenity", amenity_id)
    if s is None:
        abort(404)
    return jsonify(s.to_json())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Example endpoint deleting one amenity
    Deletes a review based on the amenity_id
    ---
    definitions:
      Amenity:
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
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Example endpoint Creates an amenity
    Creates an amenity based on amenity_id with the JSON body
    ---
    definitions:

      Amenity:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          email:
            type: string
          first_name:
            type: string
          last_name:
            type: string
          id:
            type: string
            description: the id of the user
          updated_at:
            type: string
            description: The date the object was updated
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A list of dicts or dict, each dict is an amenity
        schema:
          $ref: '#/definitions/Amenity'
        examples:
            [{"__class__": "Amenity",
              "created_at": "2017-03-25T02:17:06",
              "id": "cf701d1a-3c19-4bac-bd99-15321f1140f2",
              "name": "Dog(s)",
              "updated_at": "2017-03-25T02:17:06"}]
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    s = Amenity(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """Example endpoint updates an amenity
    Updates an amenity based on amenity_id with the JSON body
    ---
    definitions:

      Amenity:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          email:
            type: string
          first_name:
            type: string
          last_name:
            type: string
          id:
            type: string
            description: the id of the user
          updated_at:
            type: string
            description: The date the object was updated
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of a dict, the dict is an amenity
        schema:
          $ref: '#/definitions/Amenity'
        examples:
            [{"__class__": "Amenity",
              "created_at": "2017-03-25T02:17:06",
              "id": "cf701d1a-3c19-4bac-bd99-15321f1140f2",
              "name": "Dog(s)",
              "updated_at": "2017-03-25T02:17:06"}]
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    for k in ("id", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(a, k, v)
    a.save()
    return jsonify(a.to_json()), 200
