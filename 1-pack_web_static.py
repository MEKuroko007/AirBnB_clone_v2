#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the contents
# of the web_static folder of your AirBnB Clone repo

from fabric.api import local
import os
from datetime import datetime


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file_name = f"web_static_{dt.strftime('%Y%m%d%H%M%S')}.tgz"
    file_path = os.path.join("versions", file_name)

    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

    if local(f"tar -cvzf {file_path} web_static").failed is True:
        return None

    return file_path
