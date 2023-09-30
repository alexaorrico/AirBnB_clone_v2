from flask import Flask, jsonify
from api.v1.views import app_views
from models.engine import storage
from models.base_model import BaseModel


@app_views.route('/status', methods=['GET'])
def status():
    """
    return json string indication the status_code
    """
    return jsonify({"status": "OK"})
