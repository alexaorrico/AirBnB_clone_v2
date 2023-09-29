from api.v1.views import app_views
from flask import Flask

"""
    index
"""


@app_views.route("/status")
def status():
    """ status """
    return '{"status": "OK"}'
