#!/usr/bin/python3
"""Home pagae"""

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    return {
        "status": "OK"
    }
