"""Handles Functionalities and importations"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def return_status_toJson():
    """ returns a JSON: "status": "OK """
    status = {
        "status": "OK"
    }
    return jsonify(status)


