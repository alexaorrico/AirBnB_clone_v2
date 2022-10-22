
#!/usr/bin/python3
"""
route api index
"""
from flask import jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ check the status of route """
    return jsonify({'status': 'OK'})
