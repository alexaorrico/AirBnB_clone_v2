#!/usr/bin/python3
"""comment"""
from flask import Blueprint, render_template, abort
from api.v1.views.index import *
app_views = Blueprint(url_prefix="/api/v1")
