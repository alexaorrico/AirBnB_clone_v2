#!/usr/bin/python3
'''index for the api app'''


from api.v1.views import app_views
from flask import jsonify

jb = {
  "status": "OK"
}


@app_views.route('/status')
def status():
    '''returns json to the route'''
    return jsonify(jb)
