from api.v1.views import app_views
from flask import jsonify


app_views.route('/status', strict_slashes=False)


def status():
    """ returns a JSON: "status": OK """
    return({status: "OK"})
