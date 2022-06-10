#!/usr/bin/python3
""" Amenity view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """
    Retrieves the list of all Amenity objects
    ---
    tags:
      - Amenity
    responses:
      200:
        description: List of all Amenity objects
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
              created_at:
                type: string
              id:
                type: string
              name:
                type: string
              updated_at:
                type: string
          example:
            [
              {
                "__class__": "Amenity",
                "created_at": "2022-05-31T20:42:53.350872",
                "id": "244ecd41-767a-48ed-a5a2-6c9ae1e1e0a0",
                "name": "Pets friendly",
                "updated_at": "2022-05-31T20:42:53.350872"
              },
              {
                "__class__": "Amenity",
                "created_at": "2022-05-31T20:42:53.350872",
                "id": "d8476354-2489-4f2c-8075-2596adf8a2d6",
                "name": "Air conditioning",
                "updated_at": "2022-05-31T20:42:53.350872"
              }
            ]
    """
    amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """
    Retrieves a Amenity object
    ---
    tags:
      - Amenity
    parameters:
      - name: amenity_id
        in: path
        required: true
    responses:
      200:
        description: Amenity found
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "Amenity"
            created_at: "2022-05-31T20:42:53.350872"
            id: "244ecd41-767a-48ed-a5a2-6c9ae1e1e0a0"
            name: "Pets friendly"
            updated_at: "2022-05-31T20:42:53.350872"
      404:
        description: No amenity found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object
    ---
    tags:
      - Amenity
    parameters:
      - name: amenity_id
        in: path
        required: true
    responses:
      200:
        description: Amenity deleted
        schema:
          type: object
      404:
        description: No amenity found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity
    ---
    tags:
      - Amenity
    parameters:
      - name: create_amenity
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
          example:
            name: "Pool"
    responses:
      201:
        description: Amenity created
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "Amenity"
            created_at: "2022-05-31T20:42:53.350872"
            id: "1ad0edc7-9d80-4053-9166-b40f3063cbf7"
            name: "Pool"
            updated_at: "2022-05-31T20:42:53.350872"
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not a JSON"
    """
    new_amenity = request.get_json()
    if new_amenity is None:
        abort(400, 'Not a JSON')
    if 'name' not in new_amenity:
        abort(400, 'Missing name')
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    Updates a Amenity object
    ---
    tags:
      - Amenity
    parameters:
      - name: amenity_id
        in: path
        required: true
      - name: update_amenity
        description: Amenity's information to be updated
        in: body
        required: true
        example:
          {
            "name": "Gym"
          }
    responses:
      200:
        description: Amenity updated
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "Amenity"
            created_at: "2022-05-31T20:42:53.350872"
            id: "1ad0edc7-9d80-4053-9166-b40f3063cbf7"
            name: "Pool"
            updated_at: "2022-05-31T20:42:53.350872"
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not a JSON"
      404:
        description: No amenity found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    request_json = request.get_json()
    if request_json is None:
        abort(400, "Not a JSON")
    for key, value in request_json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
