from api.v1.views import app_views


@app_views.route('/status')
def status():
    """represents the route /status"""
    return {"status": "OK"}
