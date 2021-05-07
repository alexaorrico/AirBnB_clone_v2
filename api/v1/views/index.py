#!/usr/bin/python3

from ..views import app_views
from flask import jsonify

@app_views.route('/status')
def jsonresponse():
    return jsonify({"status": "ok"})
