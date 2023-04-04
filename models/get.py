#!/usr/bin/env python3

from importlib import import_module
from pathlib import Path

import os

def get_models():

    def make_class_name(module_name):
        return "".join(
            (
                x.capitalize() for x in
                    module_name.split("_")
            )
        )
    THIS_FILE = Path(os.path.abspath(__file__))
    THIS_FOLDER = THIS_FILE.parent

    EXCLUDED_FILE_NAMES = ["__init__.py", THIS_FILE.name]

    class_ret_params = (
        {
            "module": ".{}".format(x),
            "class": make_class_name(x)
        } for x in (
            file.name[:file.name.index(".")] for file in THIS_FOLDER.glob("*.py")
                if file.name not in EXCLUDED_FILE_NAMES
        )
    )
    return [
        (
            vars(
                import_module(
                    params["module"],
                    THIS_FOLDER.name
                )
            ).get(params["class"])
        ) for params in class_ret_params
    ]


if __name__ == "__main__":
    pass