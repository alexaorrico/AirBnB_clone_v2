#!/usr/bin/python3
''' Python script for index '''
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def stat():
    ''' Return JSON object. '''
    return jsonify(status=OK)
