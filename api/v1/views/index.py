from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)

@app_views.route('/status', methods=['GET'])
def get_status():
    response = {"status": "OK"}
    return jsonify(response)
