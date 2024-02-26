# AirBnb clone - Tests
This directory contains all unit test cases for this project
## File structure
- [tests/test_console.py](test/test_console.py) - tests the console's functionality, documentation, and style
- **[tests/models](tests/models)** directory contains the unit tests for all classes:
  - [test_base_model.py](tests/test_models/test_base_model.py) - tests the BaseModel class' functionality, documentation, and style
  - [test_amenity.py](tests/test_models/test_amenity.py) - tests the Amenity class' functionality, documentation, and style
  - [test_city.py](tests/test_models/test_city.py) -tests the City class' functionality, documentation, and style
  - [test_place.py](tests/test_models/test_place.py) - tests the Place class' functionality, documentation, and style
  - [test_review.py](tests/test_models/test_review.py) - tests the Review class' functionality, documentation, and style
  - [state.py](tests/test_models/test_state.py) - tests the State class' functionality, documentation, and style
  - [user.py](tests/test_models/test_user.py) - tests the User class' functionality, documentation, and style
  - **[engine](/tests/models/engine)** directory contains the unit tests for all storage classes:
    - [test_file_storage.py](tests/test_models/test_file_storage.py) - tests the FileStorage class' functionality, documentation, and style
    - [test_db_storage.py](tests/test_models/test_db_storage.py) - tests the DBStorage class' functionality, documentation, and style
