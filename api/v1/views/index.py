from api.v1.views import app_views


@app_views.get('/status')
def status():
    """display, 'status': 'ok'"""
    return {'status': "ok"}
