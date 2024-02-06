#!/usr/bin/python3
from flask import Blueprint, render_template, abort
app_views = Blueprint('app_views', __name__, template_folder='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.users import *
from api.v1.views.places import *

