#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import sudo
from fabric.api import put

env.hosts = ["54.165.64.199", "54.237.13.5"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    """
    if os.path.isfile(archive_path) is False:
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Use sudo for commands that require elevated privileges
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if sudo("rm -rf /data/web_static/releases/{}/".
            format(name)).failed is True:
        return False
    if sudo("mkdir -p /data/web_static/releases/{}/".
            format(name)).failed is True:
        return False
    if sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(file, name)).failed is True:
        return False
    if sudo("rm /tmp/{}".format(file)).failed is True:
        return False
    if sudo("mv /data/web_static/releases/{}/web_static/*"
            "/data/web_static/releases/{}/".
            format(name, name)).failed is True:
        return False
    if sudo("rm -rf /data/web_static/releases/{}/web_static".
            format(name)).failed is True:
        return False
    if sudo("rm -rf /data/web_static/current").failed is True:
        return False
    if sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(name)).failed is True:
        return False

    return True
