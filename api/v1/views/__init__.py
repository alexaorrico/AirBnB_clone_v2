<<<<<<< HEAD
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
=======
#!/usr/bin/python3
""" init file """

from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
from api.v1.views.amenities import *
from api.v1.views.places import *
>>>>>>> c02c8bf79a11e249678224b436b61ec738225fff
