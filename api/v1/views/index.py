from api.v1.views import app_views
import jsonify


@app_views.route('/status')
def status():
    return jsonify({'status': 'OK'})
