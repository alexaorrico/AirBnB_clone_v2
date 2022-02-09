#!/usr/bin/python3
""" Create a new view for Place objects that handles all
    default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def allRevie(place_id):
    '''Retrieves the list of all review objects of a State:
    GET /api/v1//places/<place_id>'''

    allView = storage.get('Place', place_id)
    listReview = []
    if allView:
        for view in allView.reviews:
            listReview.append(view.to_dict())
        return jsonify(listReview)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def getReview(review_id):
    '''Retrieves a review object. :
    GET /api/v1//reviews/<review_id>'''
    view = storage.get(Review, review_id)
    if view:
        return jsonify(view.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteView(review_id):
    '''Deletes a review object:
    DELETE /api/v1/review'''
    view = storage.get(Review, review_id)
    if view:
        storage.delete(view)
        storage.save()
        return make_response(jsonify({})), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createView(place_id):
    '''Creates a review'''
    city = storage.get('Place', place_id)
    data_request = request.get_json()
    if city:
        if isinstance(data_request, dict):
            if 'user_id' in data_request.keys:
                user = storage.get('User', data_request.user_id)
                if user:
                    for k in data_request.keys():
                        if k == "name":
                            obj = Place(**data_request)
                            storage.new(obj)
                            storage.save()
                            return jsonify(obj.to_dict()), 201
                        else:
                            abort(400, 'Missing text')
                else:
                    abort(404)
            else:
                abort(400, 'Missing user_id')
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def updateView(review_id):
    '''Updates a review object:
    PUT /api/v1/reviews/<review_id>'''
    obj = storage.get(Review, review_id)
    if obj:
        data_request = request.get_json()
        if isinstance(data_request, dict):
            noKeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)
