from zipfile import ZipFile
import json
from textwrap import wrap

def get_assets(jar_path: str) -> list[dict]:
    with ZipFile(jar_path, 'r') as jar:
        default_data: dict = json.loads(jar.read("assets/minecraft/font/include/default.json"))
        providers: list[dict] = default_data["providers"]
        for provider in providers:
            texture_path: str = provider["file"]
            texture_path = texture_path.replace("minecraft:", "assets/minecraft/textures/")
            provider["file"] = jar.read(texture_path)
    return providers

def build_tile_set(providers: list[dict]):
    for provider in providers:
        if "height" in provider:
            height = provider["height"]
        else:
            height = 8
        provider_chars: list[str] = provider["chars"]
        for chars in provider_chars:
            for char in chars:
                if char != "\x00":
                    print(char)


def build_as_pixel_font_converter_zip(jar_path: str):
    providers = get_assets(jar_path)
    build_tile_set(providers)