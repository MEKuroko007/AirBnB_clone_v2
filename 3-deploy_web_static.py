#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
from fabric.api import env, local, put, run
import os
from datetime import datetime

env.hosts = ["54.165.64.199", "54.237.13.5"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file_name = f"versions/web_static_{dt.strftime('%Y%m%d%H%M%S')}.tgz"
    
    if not os.path.exists("versions"):
        local("mkdir -p versions")

    if local(f"tar -cvzf {file_name} web_static").failed:
        return None

    return file_name


def do_deploy(archive_path):
    """Distributes an archive to a web server.
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
        f"mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/",
        f"rm -rf /data/web_static/releases/{name}/web_static",
        f"rm -rf /data/web_static/current",
        f"ln -s /data/web_static/releases/{name}/ /data/web_static/current"
    ]

    for command in commands:
        if run(command).failed:
            return False

    return True


def deploy():
    """Create and distribute an archive to a web server."""
    archive_path = do_pack()
    
    if archive_path is None:
        return False
    
    return do_deploy(archive_path)
