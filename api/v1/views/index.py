#!/usr/bin/python3
from api.v1.views.__init__ import *

moochila()

@app_views.route('/api/v1/status')
def status():
    json = {'status': 'OK'}
    return json
