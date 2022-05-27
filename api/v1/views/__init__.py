#!/usr/bin/python3
""""""
from flask import Blueprint


app_views = Blueprint('/api/v1')
# La intranet dice que PEP 8 se va a quejar por el orden de la importación 
# pero que este módulo no se va a checkear
from api.v1.views import *
from api.v1.views import index
