#!/usrbin/python3
'''Contains the index view for the API.'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    '''Gets the status of the API.
    '''
    return jsonify(status='OK')
