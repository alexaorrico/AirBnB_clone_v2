#!/usr/bin/python3

from api.v1.views import app_views

@app_views('/status')
def status():
    return {"status": "OK"}
