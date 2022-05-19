#!/usr/bin/python3
"""
init file of views
"""
from flask import Blueprint


app_views = Blueprint(
    'simple_page',
    __name__,
    url_prefix='/api/v1'
)
