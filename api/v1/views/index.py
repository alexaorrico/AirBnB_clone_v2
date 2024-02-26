#!/usr/bin/python3
from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage


@app_views.app_errorhandler(404)
def err(e):
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

@app_views.route('/status', methods = ['GET'] , strict_slashes= False)
def show_status():
    """returns the api status"""
    return jsonify({'status': 'ok'})

@app_views.route('/stats', methods= ['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    objs = storage.all().values()
    obdict = {}
    print(objs)
    for obj in objs:
        clsname = obj.__class__.__name__
        try:
            obdict[clsname] += 1
        except KeyError:
            obdict[clsname] = 1
        
    return  jsonify(obdict)
