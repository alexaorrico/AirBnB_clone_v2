#!/usr/bin/python3
""" Status of your API"""
from flask import Flask
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
