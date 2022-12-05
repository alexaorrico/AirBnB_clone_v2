#!/usr/bin/python3
from flask import Blueprint, render_template, abort
import api.v1.views.index

app_views = Blueprint(url_prefix='/api/v1')
