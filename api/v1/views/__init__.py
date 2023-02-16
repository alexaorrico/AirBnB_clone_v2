#!/usr/bin/python3

"""View module"""
from flask import Blueprint

app_views = Blueprint("api", __name__, url_prefix="/api/v1")
