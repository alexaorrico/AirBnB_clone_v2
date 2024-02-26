#!/usr/bin/python3
"""
Index file
"""

from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage


@app_views.app_errorhandler(404)
def err_404(e):
    """error handler for 404"""
    resp = make_response(jsonify({'error': 404}))
    resp.status_code = 404
    return resp


@app_views.app_errorhandler(400)
def err_400(e):
    """error handler for 400"""
    resp = make_response(jsonify({'error': 'Not a JSON'}))
    resp.status_code = 400
    return resp


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def show_status():
    """returns the api status"""
    resp = make_response(jsonify({'status': 'ok'}))
    resp.status_code = 200
    return resp


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    objs = storage.all().values()
    obdict = {}
    for obj in objs:
        clsname = obj.__class__.__name__
        try:
            obdict[clsname] += 1
        except KeyError:
            obdict[clsname] = 1

    resp = make_response(jsonify(obdict), 200)
    return resp
