#!/usr/bin/python3
# distribute an archive to a web server by using fabric.
from fabric.api import env, put, run
import os.path

env.hosts = ["54.165.64.199", "54.237.13.5"]


def do_deploy(archive_path):
    """distributes an archive to your web servers,
       using the function do_deploy
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    if put(archive_path, f"/tmp/{file_name}").failed:
        return False

    commands = [
        f"rm -rf /data/web_static/releases/{name}/",
        f"mkdir -p /data/web_static/releases/{name}/",
        f"tar -xzf /tmp/{file_name} -C /data/web_static/releases/{name}/",
        f"rm /tmp/{file_name}",
        f"mv /data/web_static/releases/{name}/web_static/*"
        f"/data/web_static/releases/{name}/",
        f"rm -rf /data/web_static/releases/{name}/web_static",
        f"rm -rf /data/web_static/current",
        f"ln -s /data/web_static/releases/{name}/ /data/web_static/current"
    ]

    for command in commands:
        if run(command).failed:
            return False

    return True
