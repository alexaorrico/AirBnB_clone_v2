#!/usr/bin/python3
"""Initializes package views"""

from flask import Blueprint, render_template, abort

app_views = Blueprint('app_views', __name__, template_folder='templates')

from api.v1.views.index import*
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.users impory *
from api.v1.views.states import *
