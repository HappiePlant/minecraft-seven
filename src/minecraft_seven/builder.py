import io
from zipfile import ZipFile
import json
from textwrap import wrap
from PIL import Image

def get_assets(jar_path: str) -> list[dict]:
    with ZipFile(jar_path, 'r') as jar:
        default_data: dict = json.loads(jar.read("assets/minecraft/font/include/default.json"))
        providers: list[dict] = default_data["providers"]
        for provider in providers:
            texture_path: str = provider["file"]
            texture_path = texture_path.replace("minecraft:", "assets/minecraft/textures/")
            provider["file"] = jar.read(texture_path)
    return providers

def build_tileset(providers: list[dict]):
    tileset = Image.new("RGBA", (10000, 12), color=(255, 0, 0, 0))
    glyphs: str = ""
    tileset_x = tileset_y = 0
    for provider in providers:
        font_img = Image.open(io.BytesIO(provider["file"]))
        font_x = font_y = 0
        if "height" in provider:
            char_height = provider["height"]
        else:
            char_height = 8
        char_width = 8
        provider_chars: list[str] = provider["chars"]
        for chars in provider_chars:  # "abcdefghij"
            for char in chars:  # "a"
                if char != "\x00":
                    char_img = font_img.crop((font_x, font_y, font_x + char_width, font_y + char_height))
                    tileset.paste(char_img, (tileset_x, tileset_y))
                    glyphs += char
                font_x += char_width
                tileset_x += char_width
            font_x = 0
            font_y += char_height
    tileset.save("out/tileset.png")


def build_as_pixel_font_converter_zip(jar_path: str):
    providers = get_assets(jar_path)
    build_tileset(providers)