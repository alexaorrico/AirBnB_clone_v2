#!/usr/bin/python3
"""
import app_views and create a route /status
"""
from api.v1.views import app_views


app.register_blueprint(app_views, url_prefix="/oak")
