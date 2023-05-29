# AirBnB clone - RESTful API
This directory contains Flask web applications for a RESTful API
## File Structure
- **[v1](v1)** directory contains the first version of the API
  - [app.py](v1/app.py) runs the Flask web application
  - **[views](v1/views)** directory contains all of the views for the Flask web application
    - [amenities.py](v1/views/amenities.py) contains the view for Amenity objects
    - [cities.py](v1/views/cities.py) contains the view for City objects
    - [index.py](v1/views/index.py) contains the view for stats and statuses
    - [places.py](v1/views/places.py) contains the view for Place objects
    - [place_amenities.py](v1/views/place_amenities.py) contains the view for Amenities objects by Place
    - [place_reviews.py](v1/views/place_reviews.py) contains the view for Reviews objects by Place
    - [states.py](v1/views/states.py) contains the view for State objects
    - [users.py](v1/views/users.py) contains the view for User objects
