#!/usr/bin/python3
"""index page status"""

from api.v1.views import app_views

@app_views.route("/status", strict_slashes=False)
def status():
    return '{\n\t"status": "ok"\n}'
