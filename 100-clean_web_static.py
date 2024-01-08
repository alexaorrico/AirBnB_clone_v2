#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""a Fabric script (based on the file 3-deploy_web_static.py) that deletes
out-of-date archives, using the function
"""

from fabric.api import put, run, env, local
from os.path import exists
from datetime import datetime

env.hosts = ["35.175.134.9", "35.153.33.206"]


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    local("mkdir -p versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    tgz_file = "versions/web_static_{}.tgz".format(timestamp)

    result = local("tar -cvzf {} web_static".format(tgz_file))

    if result.succeeded:
        return tgz_file
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if exists(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[-1]
        path = "/data/web_static/releases/{}".format(file_name.split('.')[0])
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}/".format(file_name, path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(path, path))
        run("rm -rf {}/web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(path))
        run("sudo service nginx restart")
        print("New web version deployed!")
        return True
    except BaseException:
        return False


def deploy():
    """creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """deletes out-of-date archives"""
    number = int(number)
    if number == 0 or number == 1:
        number = 2
    else:
        number += 1
    local("cd versions; ls -t | tail -n +{} | xargs rm -rf --".format(number))
    run("cd /data/web_static/releases; ls -t | tail -n +{} | xargs rm -rf --".
        format(number))
