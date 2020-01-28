#!/usr/bin/python3 
# Un comentario

from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)

@app_views.route('/status')
def status():
    return jsonify({
"status": "OK"
})
