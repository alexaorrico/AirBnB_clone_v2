'''Users Routes'''
from flask import make_response, abort, request
from . import app_views
from models import storage
from models.user import User


@app_views.get('users', defaults={'user_id': None})
@app_views.get('users/<user_id>')
def retrieveUser(user_id):
    '''Gets all user or a single user'''
    if not user_id:
        data = [user.to_dict() for user in storage.all(User).values()]
    else:
        data = storage.get(User, user_id)
        if not data:
            abort(404)
        data = data.to_dict()
    return make_response(data)


@app_views.delete('users/<user_id>')
def deleteUser(user_id):
    '''Deletes a user'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response({})


@app_views.post('users')
def createUser():
    '''Creates a user'''
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('email'):
        abort(400, 'Missing email')
    if not data.get('password'):
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return make_response(user.to_dict(), 201)


@app_views.put('users/<user_id>')
def updateUser(user_id):
    '''Updates a user'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    ignored = ['id', 'email', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignored:
            if k in user.__dict__:
                setattr(user, k, v)
    user.save()
    return make_response(user.to_dict())
