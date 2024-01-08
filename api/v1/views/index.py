from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def app_status():
    return (jsonify({"status": "OK"}))

# @app_views.route("/stats")