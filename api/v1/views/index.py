#!/usr/bin/python3
"""Index file"""

from api.vi.views import app_views
from flask import jsonify
from models import storage

# Status route
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    # Returns status
    return jsonify({"status": "OK"})