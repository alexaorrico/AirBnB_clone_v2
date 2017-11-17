#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

from fabric.api import env
file1 = __import__('1-pack_web_static')
file2 = __import__('2-do_deploy_web_static')
env.hosts = ['142.44.167.228', '144.217.246.195']


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = file1.do_pack()
    if archive_path is None:
        return False
    return file2.do_deploy(archive_path)
