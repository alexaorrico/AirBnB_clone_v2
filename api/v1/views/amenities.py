#!/usr/bin/python3
"""
file for "/api/v1/amenities" API
with GET, POST, PUT and DELETE
for getting, posting, putting and deleting
Amenity objects in 'storage', imported from
'models', and saving those changes in the
'storage's database/JSON file.
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route(
        "/amenities",
        strict_slashes=False
    )
def all_amenities_in_JSON():
    """
    Returns all Amenity objects in 'storage',
    as a JSON, from the values returned
    by 'storage.all(Amenity)'.
    """
    return jsonify(
        [
            amenity.to_dict()
            for amenity in
            storage.all(Amenity).values()
        ]
    )


@app_views.route(
        "/amenities/<amenity_id>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_amenity_by_id_in_JSON(amenity_id):
    """
    Returns the amenity with the 'amenity_id'
    argument and route in 'storage',
    in its JSON-serializable dict form,
    if the 'Amenity' object exists.

    Raises 404 otherwise.
    """
    result = storage.get(Amenity, amenity_id)

    if result is None:
        abort(404)

    return jsonify(result.to_dict())


@app_views.route(
        "/amenities/<amenity_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
def delete_amenity_by_id(amenity_id):
    """
    Deletes 'Amenity' object with 'amenity_id' as its 'id'
    field/column value (let's call it 'target')
    from 'storage.all' dictionary, by calling storage.delete(<target>).

    Returns ({}, 200) if successful,
    404 if 'target' doesn't exist.
    """
    target = storage.get(Amenity, amenity_id)

    if target is None:
        abort(404)
    storage.delete(target)
    storage.save()

    return jsonify({}), 200


@app_views.route(
        "/amenities/",
        strict_slashes=False,
        methods=["POST"]
    )
def post_amenity_in_JSON():
    """
    Creates new 'Amenity' object based on
    JSON input and the 'Amenity' and 'BaseModel'
    constructors (these constructors are in
    <project root>/models/).

    If the input provided isn't valid JSON
    or if the JSON provided has no 'name' key,
    this function calls 'flask.abort(400)',
    with a message of what went wrong:
    either "Not a JSON" or "Missing name".
    """
    new_amenity_in_JSON = request.get_json(silent=True)
    # If the request's JSON isn't valid,
    # 'new_amenity_in_JSON' is None.
    if new_amenity_in_JSON is None:
        abort(400, "Not a JSON")

    if 'name' not in new_amenity_in_JSON:
        abort(400, "Missing name")

    new_amenity = Amenity(**new_amenity_in_JSON)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>",
        strict_slashes=False,
        methods=["PUT"]
    )
def put_amenity_in_JSON(amenity_id):
    """
    Overrides 'Amenity' object's 'name' field,
    where the object's id is 'amenity_id',
    with the json attributes provided in the
    PUT request.

    If the amenity with 'amenity_id' as its 'id'
    doesn't exist, this function calls
    abort(404).

    Otherwise, this function returns the JSON
    format of the new amenity with code 200.
    """
    if storage.get(Amenity, amenity_id) is None:
        abort(404)

    new_amenity_info = request.get_json(silent=True)
    # If the request's JSON isn't valid,
    # 'new_amenity_in_JSON' is None.
    if new_amenity_info is None:
        abort(400, "Not a JSON")

    amenity = storage.get(Amenity, amenity_id)
    # 'amenity' acts like a "pointer" to the 'Amenity' object,
    # so it doesn't need to be put back
    # in the storage.
    if 'name' in new_amenity_info:
        amenity.name = new_amenity_info['name']
    storage.save()
    # We have to re-write the object change
    # to the database/storage file,
    # so that the changes are saved
    # there too, and not just in this
    # Python object.

    return jsonify(amenity.to_dict()), 200
