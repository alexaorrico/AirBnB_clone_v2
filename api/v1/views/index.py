from flask import Flask
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)

@app_views.route('/status', methods=['GET'])
def get_status():
    response = {"status": "OK"}
    return jsonify(response)
