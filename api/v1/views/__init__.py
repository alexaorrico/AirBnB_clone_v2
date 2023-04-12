#!/usr/bin/python3
""" __init__ module for app_views"""
from flask import Blueprint, Flask, abort, render_template

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *