<<<<<<< HEAD
  
#!/usr/bin/python3
"""Init file for views module"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
=======
#!/usr/bin/python3
"""
module that uses blueprint to generate app view
"""

from flask import Blueprint

app_views = Blueprint('app_view', __name__, url_prefix='/api/v1/')

from api.v1.views.index import *
from api.v1.views import states, cities, amenities, users
from api.v1.views import places, places_reviews
>>>>>>> master
