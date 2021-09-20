#!/usr/bin/python3
from flask import Blueprint
app_views = Blueprint(
    					'app_views', # the blueprint name
                    	__name__, # related to what! (states/cities ..)
                    	url_prefix='/api/v1' #clear!
                      )

from api.v1.views.index import *
from api.v1.views.cities import *