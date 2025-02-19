from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Return the status of the API.

    Returns:
        A JSON object containing the status of the API.
    """
    return {'status': 'OK'}
