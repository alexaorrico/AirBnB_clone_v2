#!/usr/bin/python3
"""Initialize Blueprint views"""
from flask import Flask
from flask import Blueprint
import * from api.v1.views.index


#create a variable app_views which is an instance of Blueprint (url prefix must be /api/v1)
app_views = Blueprint("app", __name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
