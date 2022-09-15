#!/usr/bin/python3
""" something for now"""

from flask import Flask, Blueprint, render_template
from models import storage
from api.v1.views import app_view



app = Flask(__name__)
