from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})

@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    return jsonify(storage.count())
