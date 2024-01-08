from api.v1.views import app_views

@app_views.route("/status")
def status():
    """Return status"""
    return {"status": "OK"}