from . import app_views

@app_views.route('/status')
def status():
    return {"status":"OK"}
