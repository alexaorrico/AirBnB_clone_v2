#!/usr/bin/python3
"""deploy archive"""
import os
import tarfile
from datetime import datetime
from fabric.api import local, env, run, put


env.hosts = ['54.237.18.57', '54.234.41.234']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id.rsa'


def do_pack():
    """generate .tgz archive from folder content"""
    date = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(date.year,
                                                         date.month,
                                                         date.day,
                                                         date.hour,
                                                         date.minute,
                                                         date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """deplooooooooy"""
    f = archive_path.split('/')[1]
    try:
        put(archive_path, '/tmp/{}'.format(f))
        run('mkdir -p /data/web_static/releases/{}'.format(f))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(f, f))
        run('rm /tmp/{}'.format(f))
        run('mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/'.format(f, f))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(f))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/\
        /data/web_static/current'.format(f))
        print("New version deployed!")
        return True
    except:
        print("New version not deployed...")
        return False
