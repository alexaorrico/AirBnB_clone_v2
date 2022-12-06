#!/usr/bin/python3
from flask import Blueprint, render_template, abort
from api.v1.views.index import *

app_views = Blueprint('app_view', __name__, url_prefix='/api/v1')
