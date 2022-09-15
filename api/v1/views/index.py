#!/usr/bin/python3

"""Comments"""

import json
from api.v1.views import app_views

@app_views.route("/status", strict_slashes=False)
def status_ok():
    return json.loads('{"status": "OK"}')
