from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def hello_hbnb():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})
