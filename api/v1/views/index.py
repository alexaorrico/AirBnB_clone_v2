from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def view_status():
    """Show Ok status"""
    return jsonify({"status": "OK"})
