#!/usr/bin/python3

"""Importation of Blueprint in flask and a module"""
from flask import Blueprint
from api.v1.views.index import *

"""creating  a variable which is an instance of Blueprint class"""
app_views = Blueprint("app_views", __name__, template_folder="/api/v1")
