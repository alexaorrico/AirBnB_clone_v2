#!/usr/bin/python3
from api.v1.views import app_views
from flask import Blueprint
from flask import jsonify

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
