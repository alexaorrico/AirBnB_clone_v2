# api/__init__.py
from flask import Flask
from api.v1.app import app as app_v1

app = Flask(__name__)

app.register_blueprint(app_v1, url_prefix='/api/v1')
