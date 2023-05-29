<<<<<<< HEAD
  
=======
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
>>>>>>> 8f3d9dee79eec5dc4c542470ee31a868f377a9fc
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
<<<<<<< HEAD
from api.v1.views.places_amenities import *

=======
from api.v1.views.states import *
from api.v1.views.users import *
>>>>>>> 778ea08ab0a36aadb0a62f27b5459c789b64051d
>>>>>>> 8f3d9dee79eec5dc4c542470ee31a868f377a9fc
