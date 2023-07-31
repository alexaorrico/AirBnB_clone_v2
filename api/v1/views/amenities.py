"""State view for the web service API"""
from flask import jsonify, abort, request
from api.v1.views import app_views  # Blueprint object
from models import storage
from models.amenity import Amenity


# Route to get Amenity
@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenities(amenity_id=None):
    """Return a JSON reponse of all amenity objects,
        or object of a specified id
    """

    amenity_objs = []  # To store list of all amenity objects dictionary
    if amenity_id:
        # Get dictionary of amenity object by id
        amenity_objs.append((storage.get(Amenity, amenity_id)).to_dict())
    else:
        objects = storage.all(Amenity)  # Get amenity objects
        for key in objects:
            # get dictionary of amenity objects
            amenity_objs.append(objects[key].to_dict())

    if len(amenity_objs) == 0:
        abort(404)
    else:
        return jsonify(amenity_objs)


# Route to delete an amenity object
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """Delete an amenity object specified by it id"""

    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)

        if not amenity:
            abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

# Route to create an amenity object


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Create a new amenity object"""

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    if 'name' not in content:
        abort(400, 'Missing name')  # raise bad request error
    amenity = Amenity(**content)
    amenity.save()

    return jsonify(amenity.to_dict()), 201

# Route to update an amenity object


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Update an amenity object specified by id"""

    amenity = storage.get(Amenity, amenity_id)  # Get amenity by id

    if not amenity:
        abort(404)  # raise not found error

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    for key, value in content.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)  # Update amenity with new data
            amenity.save()

    return jsonify(amenity.to_dict()), 200
