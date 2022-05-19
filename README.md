# <div align="center">AirBnB clone - The console</div>

## Description
This is the first step towards building our first full web application with **Holberton School**.

This part of the project implements a command-line interface for data management.

## Usage of the console

The [console](https://github.com/Anna78990/AirBnB_clone/blob/main/console.py) prints a prompt "**(hbnb)** " and waits for the user for input. It works in interactive mode and non-interactive mode.

| Command          | Example |
| ------------- |:-------------:|
| Run the command   | ```./console.py```|
| Display the help for a command | ```(hbnb) help <command>```|
| Create an object     | ```(hbnb) create <class name>```    |
| Show the content of an object | ```(hbnb) show <class name> <id>``` |
| Show all objects or all instances of a class | ```(hbnb) all``` or ```(hbnb) all <class name>``` |
| Update an attribute of an object | ```(hbnb) update <class name> <id> <attribute name> <value>``` |
| Destroy an object | ```(hbnb) destroy <class name> <id>``` |
| Quit the console | ```(hbnb) quit``` or ```(hbnb) EOF``` |

Example of output :

```
(hbnb) create BaseModel
493a5ba7-a9d9-436b-bd96-6d6838d939b3
(hbnb) show BaseModel 493a5ba7-a9d9-436b-bd96-6d6838d939b3
[BaseModel] (493a5ba7-a9d9-436b-bd96-6d6838d939b3) {'id': '493a5ba7-a9d9-436b-bd96-6d6838d939b3', 'created_at': datetime.datetime(2022, 3, 4, 11, 53, 22, 266531), 'updated_at': datetime.datetime(2022, 3, 4, 11, 53, 22, 266544)}
(hbnb) create User
f075111a-53f9-45e4-a7c4-f76260408e8e
(hbnb) all
["[BaseModel] (d78b1b3e-17e6-4ebf-8de2-2e08bda508b7) {'id': 'd78b1b3e-17e6-4ebf-8de2-2e08bda508b7', 'created_at': datetime.datetime(2022, 3, 3, 16, 12, 51, 590511), 'updated_at': datetime.datetime(2022, 3, 3, 16, 12, 51, 590526)}", "[BaseModel] (493a5ba7-a9d9-436b-bd96-6d6838d939b3) {'id': '493a5ba7-a9d9-436b-bd96-6d6838d939b3', 'created_at': datetime.datetime(2022, 3, 4, 11, 53, 22, 266531), 'updated_at': datetime.datetime(2022, 3, 4, 11, 53, 22, 266544)}", "[User] (f075111a-53f9-45e4-a7c4-f76260408e8e) {'id': 'f075111a-53f9-45e4-a7c4-f76260408e8e', 'created_at': datetime.datetime(2022, 3, 4, 11, 55, 13, 845017), 'updated_at': datetime.datetime(2022, 3, 4, 11, 55, 13, 845029)}"]
(hbnb) update User f075111a-53f9-45e4-a7c4-f76260408e8e first_name "Betty"
(hbnb) show User f075111a-53f9-45e4-a7c4-f76260408e8e
[User] (f075111a-53f9-45e4-a7c4-f76260408e8e) {'id': 'f075111a-53f9-45e4-a7c4-f76260408e8e', 'created_at': datetime.datetime(2022, 3, 4, 11, 55, 13, 845017), 'updated_at': datetime.datetime(2022, 3, 4, 11, 55, 13, 845029), 'first_name': 'Betty'}
(hbnb) destroy User f075111a-53f9-45e4-a7c4-f76260408e8e
(hbnb) all
["[BaseModel] (d78b1b3e-17e6-4ebf-8de2-2e08bda508b7) {'id': 'd78b1b3e-17e6-4ebf-8de2-2e08bda508b7', 'created_at': datetime.datetime(2022, 3, 3, 16, 12, 51, 590511), 'updated_at': datetime.datetime(2022, 3, 3, 16, 12, 51, 590526)}", "[BaseModel] (493a5ba7-a9d9-436b-bd96-6d6838d939b3) {'id': '493a5ba7-a9d9-436b-bd96-6d6838d939b3', 'created_at': datetime.datetime(2022, 3, 4, 11, 53, 22, 266531), 'updated_at': datetime.datetime(2022, 3, 4, 11, 53, 22, 266544)}"]
(hbnb) quit
```
## Classes

The folder [models](https://github.com/Anna78990/AirBnB_clone/tree/main/models) contains all the classes:

|   | [BaseModel](./models/base_model.py) | [User](./models/user.py) | [State](./models/state.py) | [City](./models/city.py) | [Place](./models/place.py) | [Amenity](./models/amenity.py) | [Review](./models/review.py) |
| :--------: | :--------: | :--------: |:--------: | :--------: | :--------: |:--------: | :--------: |
| **Description** | Base model class for other classes | User class for future user informations | State class for future location informations | City class for future location informations | Place class for future location informations | Amenity class for future amenity information | Review class for future review information |
| **Public Instance Attributes** | ```id``` ```create_at``` ```updated_at``` | Inherits from ```BaseModel``` | Inherits from ```BaseModel```|Inherits from ```BaseModel```|Inherits from ```BaseModel```|Inherits from ```BaseModel```|Inherits from ```BaseModel```|
| **Public Instance Methods** | ```save``` ```to_dict``` ```__str__``` |  
| **Public Class Attributes** | | ```email``` ```password``` ```first_name``` ```last_name``` | ```name``` | ```state_id``` ```name``` | ```city_id``` ```user_id``` ```name``` ```description``` ```number_rooms``` ```number_bathrooms``` ```max_guest``` ```price_by_night``` ```latitude``` ```longitude``` ```amenity_ids``` | ```name``` | ```place_id``` ```user_id``` ```text``` |

## File Storage

The folder [engine](https://github.com/Anna78990/AirBnB_clone/tree/main/models/engine) manages the serialization and deserialization of all the data, following a JSON format.

The FileStorage class found in the [file_storage.py](https://github.com/Anna78990/AirBnB_clone/blob/main/models/engine/file_storage.py) follows the flow of serialization-deserialization like this :
```<object> -> to_dict() -> <class 'dict'> -> JSON dump -> <class 'str'> -> FILE -> <class 'str'> -> JSON load -> <class 'dict'> -> <object>```

The [init.py](https://github.com/Anna78990/AirBnB_clone/blob/main/models/__init__.py) file contains the instantiation of the class FileStorage called storage and the call of the method reload(). This allows to retrieve all data from the initialization.

## Tests

All the files are tested with the unittest module and are in the [test_models](https://github.com/Anna78990/AirBnB_clone/tree/main/tests/test_models).

## Authors

- Maxence Potier : [GitHub](https://github.com/Mxn-ptr) - [LinkedIn](https://www.linkedin.com/in/maxence-potier-534b0a1b0/) - Mail : 3633@holbertonschool.com

- Jordan Mpounza : [GitHub](https://github.com/ozswar94) - [LinkedIn](https://www.linkedin.com/in/jordan-mpounza) - Mail : 3630@holbertonschool.com
