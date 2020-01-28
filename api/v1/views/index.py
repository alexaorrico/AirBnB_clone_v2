from api.v1.views import app_views
from json import dumps
from flask import jsonify

@app_views.route('/status')
def status():

    return jsonify({"status": "OK"})
