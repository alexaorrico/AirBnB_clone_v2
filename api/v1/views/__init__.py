#!/usr/bin/python3
# This is the init page

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
