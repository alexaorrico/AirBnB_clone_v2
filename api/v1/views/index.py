#!/usr/bin/python3

from api.v1.views import app_views
from flask.json import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status of API """
    return jsonify({'status': 'OK'})
