from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

app_views = Blueprint('app_views', __name__,
                      url_prefix='/api/v1')

from api.v1.views.index import *
