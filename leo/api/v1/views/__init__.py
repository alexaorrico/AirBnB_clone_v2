from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/app/vi')


from api.vi.views.index import *
