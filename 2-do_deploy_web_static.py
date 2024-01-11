#!/usr/bin/python3
# distribute an archive to a web server by using fabric.
from fabric.api import env, put, run
import os

env.hosts = ["54.165.64.199", "54.237.13.5"]


def do_deploy(archive_path):
    """Distributes an archive to a web server."""

    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("rm -rf /data/web_static/releases/{}/".format(name))
        run("mkdir -p /data/web_static/releases/{}/".
            format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(file_name, name))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/*"
            "/data/web_static/releases/{}/".
            format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(name))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
