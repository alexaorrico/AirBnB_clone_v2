from views import app_views


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Returns a JSON"""
    return {"status": "OK"}
