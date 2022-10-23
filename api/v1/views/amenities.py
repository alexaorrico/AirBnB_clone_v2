"""Module amenities.py: contains amenities information"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities/<amenity_id>',
				 methods=['GET', 'DELETE', 'PUT'],
				 strict_slashes=False)
def amenity(amenity_id):
	"""returns an amenity based on it's id"""
	for amenity in storage.all(Amenity).values():
		if amenity.id == amenity_id:
			if request.method == 'DELETE':
				amenity.delete()
				storage.save()
				return '{}'

			elif request.method == 'PUT':
				res = request.get_json()
				if res is None:
					abort(400, description='Not a JSON')
				for k, v in res.items():
					if k.endswith('ed_at') or k == 'state_id' or k == 'id':
						continue
					setattr(amenity, k, v)
				amenity.save()

			return jsonify(amenity.to_dict())

	abort(404)


@app_views.route('/amenities',
				 methods=['GET', 'POST'],
				 strict_slashes=False)
def amenities():
	"""displays and creates an amenity"""
	if request.method == 'POST':
		res = request.get_json()
		if res is None:
			abort(400, description='Not a JSON')
		if 'name' not in res.keys():
			abort(400, description='Missing name')

		new_amenity = Amenity(**res)
		new_amenity.save()
		return jsonify(new_amenity.to_dict()), 201

	amenity = [v.to_dict() for v in storage.all(Amenity).values()]
	return jsonify(amenity)