from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def json_string():
    new = {}
    new['status'] = "OK"
    return jsonify(new)
