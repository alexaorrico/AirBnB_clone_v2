#!/usr/bin/python3
#import api.v1.views
from flask import Flask
from api.v1.views import app_views
from json import dumps, loads


@app_views.route('/status')
def status():
    """returns status ok"""
    return (loads('{"status": "OK"}'))
