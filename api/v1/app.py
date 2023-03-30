#!/usr/bin/python3
"""App"""
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
