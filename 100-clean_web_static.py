#!/usr/bin/python3
# keep it clean
import os
from fabric.api import local, env, run, lcd, cd


env.hosts = ["54.144.250.63", "34.224.15.29"]


def do_clean(number=0):
    """clean archives"""
    number = 1 if int(number) == 0 else int(number)

    archs = sorted(os.listdir("versions"))
    [archs.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archs]

    with cd("/data/web_static/releases"):
        archs = run("ls -tr").split()
        archs = [a for a in archs if "web_static_" in a]
        [archs.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archs]
