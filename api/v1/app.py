#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

