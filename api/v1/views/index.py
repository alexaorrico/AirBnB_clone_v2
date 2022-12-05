#!/isr/bin/python3
"""
Module index
"""
from api.v1.views import app_views
import json


@app_views.route('/status')
def status_route():
        my_dict = {"Status": "OK"}
        return json.dumps(my_dict)
