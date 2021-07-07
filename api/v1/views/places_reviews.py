#!/usr/bin/python3
"""
    HBNB_V3: Task 12
"""
from api.v1.views.index import app_views, Place, Review, User
from models import storage
from flask import jsonify, request, abort, make_response


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def viewallthereviewthings(place_id):
    """Retrieves the list of all State objects"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if request.method == 'GET':
        p = storage.get(Place, place_id)
        rtl = p.reviews
        revws = [revw.to_dict() for revw in rtl]
        return jsonify(revws)
    if request.method == 'POST':
        try:
            body = request.get_json()
            if "user_id" not in body.keys():
                return "Missing user_id", 400
            elif "text" not in body.keys():
                return "Missing text", 400
            else:
                if storage.get(User, body.get('user_id')) is None:
                    return "", 404
                if storage.get(Place, place_id) is None:
                    return "", 404
                body.update({"place_id": place_id})
                newrevw = Review(**body)
                """for k in body.keys():
                    setattr(newstate, k, body.get(k))"""
                """newstate.__dict__.update(body)"""
                newrevw.save()
                return jsonify(newrevw.to_dict()), 201
        except:
            return "Not a JSON", 400


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def reviewidtime(review_id):
    """Handles a state object with said id depending on HTTP request"""
    rtl = storage.get(Review, review_id)
    if rtl is not None:
        sd = rtl.to_dict()
        if request.method == 'GET':
            return jsonify(sd)
        if request.method == 'DELETE':
            storage.delete(rtl)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            try:
                body = request.get_json()
                body.pop("id", "")
                body.pop("created_at", "")
                body.pop("updated_at", "")
                body.pop("user_id", "")
                body.pop("place_id", "")
                """s.__dict__.update(body)"""
                for k in body.keys():
                    setattr(rtl, k, body.get(k))
                """s.save()"""
                rtl.save()
                sd = rtl.to_dict()
                return jsonify(sd)
            except:
                return "Not a JSON", 400

    else:
        abort(404)
