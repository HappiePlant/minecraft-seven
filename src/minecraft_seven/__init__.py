import os
import sys
from zipfile import ZipFile
from xdialog import open_file
import json

MINECRAFT_VERSION = "1.21"

def get_jar_path() -> str:
    jar_path: str
    if len(sys.argv) > 1:
        jar_path = sys.argv[1]
        jar_path = os.path.abspath(jar_path)
    else:
        jar_path = open_file(title="Select the 1.21 jar file", filetypes=[("JAR file", ".jar")], multiple=False)
        if jar_path == "":
            raise ValueError("Something went wrong picking the jar file")

    return jar_path

def check_minecraft_version(jar_path: str):
    with ZipFile(jar_path, "r") as jar:
        version_data = json.loads(jar.read("version.json"))
    version = version_data['id']
    if version != MINECRAFT_VERSION:
        raise Exception("Minecraft version does not match")


def main() -> None:
    jar_path = get_jar_path()
    check_minecraft_version(jar_path)


    return

if __name__ == '__main__':
    main()