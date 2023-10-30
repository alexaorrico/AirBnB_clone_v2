#!/usr/bin/env python3
"""
  Airbnb clone restful API
"""
from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv

HBNB_API_HOST = getenv("HBNB_API_HOST") or "localhost"
HBNB_API_PORT = getenv("HBNB_API_PORT") or 5000

app = Flask(__name__)
app.register_blueprint(app_views)

@app.testdown_appcontext()
def close_session():
  """ Close db session """
  storage.close()

if __name__ == "__main__":
  host = HBNB_API_HOST
  port = int(HBNB_API_PORT)
  app.run(host=host, port=port)






