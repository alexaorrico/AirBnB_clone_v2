from flask import jsonify
from api.v1.views import app_views

#return api status code
@app_views.route("/status", methods=["GET"])
def status():
    #api status code
    return jsonify({"status": "OK"})
