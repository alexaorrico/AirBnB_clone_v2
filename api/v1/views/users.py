"""Module users.py: contains users information"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage


@app_views.route('/users/<user_id>',
				 methods=['GET', 'DELETE', 'PUT'],
				 strict_slashes=False)
def user(user_id):
	"""returns an user based on it's id"""
	for user in storage.all(User).values():
		if user.id == user_id:
			if request.method == 'DELETE':
				user.delete()
				storage.save()
				return '{}'

			elif request.method == 'PUT':
				res = request.get_json()
				if res is None:
					abort(400, description='Not a JSON')
				for k, v in res.items():
					if k.endswith('ed_at') or k == 'email' or k == 'id':
						continue
					setattr(user, k, v)
				user.save()

			return jsonify(user.to_dict())

	abort(404)


@app_views.route('/users',
				 methods=['GET', 'POST'],
				 strict_slashes=False)
def users():
	"""displays and creates an user"""
	if request.method == 'POST':
		res = request.get_json()
		if res is None:
			abort(400, description='Not a JSON')
		if 'email' not in res.keys():
			abort(400, description='Missing email')

		if 'password' not in res.keys():
			abort(400, description='Missing password')


		new_user = User(**res)
		new_user.save()
		return jsonify(new_user.to_dict()), 201

	user = [v.to_dict() for v in storage.all(User).values()]
	return jsonify(user)