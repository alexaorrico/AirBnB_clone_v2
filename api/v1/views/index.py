#!/usr/bin/python3
"""  """

import json
from api.v1.views import app_views


@app_views.route('/status')
def show_status():
    """ Shows the api response status """
    return json.dumps({"status": "OK"})
