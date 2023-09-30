from flask import Blueprint, jsonify

from api.v1.views import app_views

# Define your routes within the blueprint
@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
