"""Index view for the web service API"""
from flask import jsonify
from api.v1.views import app_views  # Blueprint object


# Create the route "/status" on the Blueprint object
@app_views.route('/status')
def status():
    # Return a JSON response with the status "OK"
    return jsonify({"status": "OK"})
