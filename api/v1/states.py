#!/usr/bin/python3

from flask import Flask, request
from models import storage
from models.state import State
from api.v1.views import app_views

app = Flask(__name__)

@app.route('/states', strict_slashes=False)