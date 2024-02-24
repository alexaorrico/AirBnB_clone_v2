#!/usr/bin/python3
"""
API
"""
from models import storage
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)
