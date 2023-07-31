"""User view for the web service API"""
from flask import jsonify, abort, request
from api.v1.views import app_views  # Blueprint object
from models import storage
from models.user import User


# Route to get User
@app_views.route('/users', strict_slashes=False, methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_users(user_id=None):
    """Return a JSON reponse of all user objects,
        or object of a specified id
    """

    if user_id:
        # Get dictionary of user object by id
        user = storage.get(User, user_id)
        if user:
            return jsonify(user.to_dict())
        else:
            abort(404)
    else:
        # Get list of user objects dictionary
        user_objs = [v.to_dict() for k, v in storage.all(User).items()]
        return jsonify(user_objs)


# Route to delete user object
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Delete a user object specified by it id"""

    if user_id:
        user = storage.get(User, user_id)

        if not user:
            abort(404)
        else:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200

# Route to create a user object


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Create a new user object"""

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    if 'email' not in content:
        abort(400, 'Missing email')  # raise bad request error
    if 'password' not in content:
        abort(400, 'Missing password')  # raise bad request error
    user = User(**content)
    user.save()

    return jsonify(user.to_dict()), 201

# Route to update an amenity object


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Update a user object specified by id"""

    user = storage.get(User, user_id)  # Get user by id

    if not user:
        abort(404)  # raise not found error

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    for key, value in content.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)  # Update user with new data
            user.save()

    return jsonify(user.to_dict()), 200
