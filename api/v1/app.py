#!/usr/bin/python3
"""Create a variable app, instance of Flask"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv



app = Flask(__name__)

app.register_blueprint(app_views)


@app.route('/', methods = ['GET'])
def get_post():
  return jsonify

if __name__ == "__main__":
  app.run(debug=True)
  
  
  