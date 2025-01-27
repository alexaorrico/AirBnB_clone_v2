#!/usr/bin/python3
"""index file"""
from api.v1.views import app_views
import json


@app_views.route('/status')
def status():
	status_dict = {"status": "OK"}
	x = json.dumps(status_json, indent=2)
	return x
