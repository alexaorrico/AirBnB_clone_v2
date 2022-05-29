@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id=None):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__" and key != "id" and key != "user_id" and\
           key != "city_id" and key != "created_at" and key != "updated_at":

            setattr(place, key, value)
            storage.save()
    return jsonify(place.to_dict()), 200
