#!/usr/bin/python3
"""Module for handling Blueprint app_views"""
from flask import Blueprint, make_response, abort, request

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
