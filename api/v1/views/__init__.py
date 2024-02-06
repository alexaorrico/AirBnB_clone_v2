from flask import Blueprint
from api.v1.views.index import view1, view2, view3

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Register the view functions with the Blueprint
app_views.add_url_rule('/route1', view_func=view1)
app_views.add_url_rule('/route2', view_func=view2)
app_views.add_url_rule('/route3', view_func=view3)
