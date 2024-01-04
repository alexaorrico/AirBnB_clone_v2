#!/usr/bin/python3
"""index"""


from api.v1.views import app_views


@app_views.route('/status')
def status():
    """return status"""
    stat = {"status": "OK"}
    json_response_stat = jsonify(stat)
    return json_response_stat
