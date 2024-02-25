#!/usr/bin/python3
"""
initialize the models package
"""
import glob
from os import getenv

storage_t = getenv("HBNB_TYPE_STORAGE")


def __get_modelname_mapping():
    """Returns a `Model name` to lowercased mapping
    of all the defined models in the `models` directory."""
    model_paths = glob.glob(glob.escape("./models/") + "[a-z]*.py")
    model_mapping = {}
    for f in model_paths:
        if "base_model" in f:
            continue
        f_name = f.split("/")[-1].split(".")[0]
        capitalized_name = f_name.capitalize()
        if not f_name.endswith("y"):
            model_mapping[capitalized_name] = f_name + "s"
        else:
            model_mapping[capitalized_name] = f_name[:-1] + "ies"

    return model_mapping


model_mapping = __get_modelname_mapping()

if storage_t == "db":
    from models.engine.db_storage import DBStorage, classes
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage, classes
    storage = FileStorage()
storage.reload()
