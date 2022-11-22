#!/usr/bin/python3
""" init file which defines blueprint """
from flask import Blueprint, render_template, abort
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
