from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    ''' Returns a status in JSON format '''
    return jsonify({"status": "OK"})
