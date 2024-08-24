import argparse
import os
from zipfile import ZipFile
from xdialog import open_file
from minecraft_seven.builder import build_as_pixel_font_converter_batch
import json

MINECRAFT_VERSION = "1.21"


def get_jar_path() -> str:
    parser = argparse.ArgumentParser(description="Minecraft Seven Font Builder")
    parser.add_argument("jar_path", nargs="?", default=None)
    args = parser.parse_args()

    if args.jar_path is not None:
        jar_path: str = os.path.abspath(args.jar_path)
    else:
        jar_path = open_file(
            title="Select the 1.21 jar file",
            filetypes=[("JAR file", "*.jar")],
            multiple=False,
        )
        if jar_path == "":
            raise ValueError("Something went wrong picking the jar file")

    return jar_path


def check_minecraft_version(jar_path: str):
    with ZipFile(jar_path, "r") as jar:
        version_data = json.loads(jar.read("version.json"))
    version = version_data["id"]
    if version != MINECRAFT_VERSION:
        raise Exception("Minecraft version does not match")


def main() -> None:
    jar_path = get_jar_path()
    check_minecraft_version(jar_path)
    build_as_pixel_font_converter_batch(jar_path, MINECRAFT_VERSION)

    return


if __name__ == "__main__":
    main()
