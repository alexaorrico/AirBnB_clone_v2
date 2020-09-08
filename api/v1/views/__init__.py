from flask import Blueprint, jsonify
from api.v1.views import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1/')

status = {'status': 'ok'}
@app_views.route('/status', methods=['GET'])
def get_tasks():
    """ check the status of route """
    # return('hola')
    return jsonify({'status': 'ok'})
