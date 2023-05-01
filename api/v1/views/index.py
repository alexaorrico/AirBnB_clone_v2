#!/usr/bin/python3

"""index file for flask"""

from api.v1.views import app_views

@app.app_views('/status', strict_slashes=False)
    def api_stats():
    """function to return api status"""

        return jsonify({"status": "OK"})
