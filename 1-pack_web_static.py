#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

import os
import tarfile
from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """Generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.isdir("versions"):
            os.mkdir("versions")
        file_name = f"versions/web_static_{date}.tgz"
        with tarfile.open(file_name, "w:gz") as tar:
            tar.add("web_static")
        return file_name
    except Exception as e:
        print(f"An error occurred during archive creation: {str(e)}")
        return None
