
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def index():
    """ returns a JSON """
    return jsonify({"status": "OK"})
