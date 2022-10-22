import json

from api.v1.views import app_views


@app_views.route('/status')
def show_stats():
    return json.dumps({"status": "OK"})
