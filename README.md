Airbnb Clone - The RESTful API

The RESTful API is a key component of the Airbnb project at Holberton School, aiming to cover essential concepts of higher-level programming and web development. This segment focuses on creating a RESTful API to manage objects for the Airbnb clone (HBnB) website, enabling seamless interaction between the front-end and back-end.

Functionalities of this RESTful API:

Create a new object: Add new entries such as a new User or a new Place.
Retrieve an object: Fetch details of objects from a file, database, etc.
Perform operations on objects: Execute operations like counting and computing statistics.
Update attributes of an object: Modify the properties of an existing object.
Destroy an object: Delete an object from the database.
Table of Contents
Environment
Installation
File Descriptions
Usage
Examples of Use
Bugs
Authors
License
Environment

This project is developed and tested on Ubuntu 20.04 LTS using Python 3.8.

Installation

Clone this repository: https://github.com/Kokiben/AirBnB_clone_v3.git
Access the project directory: cd AirBnB_clone_v3
Set up a virtual environment and install dependencies: python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Set up the database: cat setup_mysql_dev.sql | mysql -u root -p
File Descriptions
 • api/: Contains the API implementation.

 • v1/: Version 1 of the API.
 • app.py: Entry point for the API.
 • views/: Contains the route handlers for different objects.
 • index.py: General routes.
 • states.py: Routes for State objects.
 • cities.py: Routes for City objects.
 • amenities.py: Routes for Amenity objects.
 • users.py: Routes for User objects.
 • places.py: Routes for Place objects.
 • reviews.py: Routes for Review objects.

 • models/: Contains classes and database storage logic.

 • base_model.py: The BaseModel class from which other classes inherit.
 • amenity.py, city.py, place.py, review.py, state.py, user.py: Classes representing different entities.
 • engine/: Storage engine implementations.
 • file_storage.py: Handles JSON file serialization and deserialization.
 • db_storage.py: Handles database interactions using MySQL.
Usage

Run the API server: HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m api.v1.app

Access the API: The API will be accessible at http://localhost:5000/api/v1/.

Examples of Use
 • Create a new user: curl -X POST http://localhost:5000/api/v1/users -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "password"}'
 • Retrieve a user: curl http://localhost:5000/api/v1/users/<user_id>
 • Update a user: curl -X PUT http://localhost:5000/api/v1/users/<user_id> -H "Content-Type: application/json" -d '{"first_name": "John"}'
 • Delete a user: curl -X DELETE http://localhost:5000/api/v1/users/<user_id>

Certainly! Here's a detailed description for your Airbnb clone API in the style of the example you provided:

Airbnb Clone - The RESTful API
The RESTful API is a key component of the Airbnb project at Holberton School, aiming to cover essential concepts of higher-level programming and web development. This segment focuses on creating a RESTful API to manage objects for the Airbnb clone (HBnB) website, enabling seamless interaction between the front-end and back-end.

Functionalities of this RESTful API:
Create a new object: Add new entries such as a new User or a new Place.
Retrieve an object: Fetch details of objects from a file, database, etc.
Perform operations on objects: Execute operations like counting and computing statistics.
Update attributes of an object: Modify the properties of an existing object.
Destroy an object: Delete an object from the database.
Table of Contents
Environment
Installation
File Descriptions
Usage
Examples of Use
Bugs
Authors
License
Environment
This project is developed and tested on Ubuntu 20.04 LTS using Python 3.8.

Installation
Clone this repository:

bash
Copy code
git clone "https://github.com/yourusername/AirBnB_clone_v2.git"
Access the project directory:

bash
Copy code
cd AirBnB_clone_v2
Set up a virtual environment and install dependencies:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Set up the database:

bash
Copy code
cat setup_mysql_dev.sql | mysql -u root -p
File Descriptions
api/: Contains the API implementation.

v1/: Version 1 of the API.
app.py: Entry point for the API.
views/: Contains the route handlers for different objects.
index.py: General routes.
states.py: Routes for State objects.
cities.py: Routes for City objects.
amenities.py: Routes for Amenity objects.
users.py: Routes for User objects.
places.py: Routes for Place objects.
reviews.py: Routes for Review objects.
models/: Contains classes and database storage logic.

base_model.py: The BaseModel class from which other classes inherit.
amenity.py, city.py, place.py, review.py, state.py, user.py: Classes representing different entities.
engine/: Storage engine implementations.
file_storage.py: Handles JSON file serialization and deserialization.
db_storage.py: Handles database interactions using MySQL.
Usage
Run the API server:

bash
Copy code
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m api.v1.app
Access the API: The API will be accessible at http://localhost:5000/api/v1/.

Examples of Use
Create a new user:

bash
Copy code
curl -X POST http://localhost:5000/api/v1/users -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "password"}'
Retrieve a user:

bash
Copy code
curl http://localhost:5000/api/v1/users/<user_id>
Update a user:

bash
Copy code
curl -X PUT http://localhost:5000/api/v1/users/<user_id> -H "Content-Type: application/json" -d '{"first_name": "John"}'
Delete a user:

bash
Copy code
curl -X DELETE http://localhost:5000/api/v1/users/<user_id>

Bugs
For any issues or bugs, please report them through the GitHub repository's issue tracker.

Authors
Kaoutar Bennassar
Mohamed El-Aroussi

License
This project is licensed under the MIT License - see the LICENSE file for details.
