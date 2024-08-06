#!/usr/bin/python3
""" module for views """

from flask import Blueprint, render_template

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
