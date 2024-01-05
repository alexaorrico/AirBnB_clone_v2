#!/usr/bin/python3

from flask import Flask, Blueprint, render_template, abort
from api.v1.views.index import *

app_views = Blueprint('app_views', url_prefix='/api/v1')
