import io
import tomllib
from zipfile import ZipFile
import json
from PIL import Image

class Provider:
    id: str
    file: bytes
    width: int
    height: int
    baseline: int
    chars: list[str]

def get_assets(jar_path: str, tile_data: dict) -> list[Provider]:
    with ZipFile(jar_path, 'r') as jar:
        default_data: dict = json.loads(jar.read("assets/minecraft/font/include/default.json"))
        providers: list[dict] = default_data["providers"]
        new_providers: list[Provider] = []
        for provider in providers:

            new_provider: Provider = Provider()
            texture_id: str = provider["file"]
            new_provider.id = texture_id
            texture_name = texture_id.replace("minecraft:", "assets/minecraft/textures/")
            new_provider.file = jar.read(texture_name)

            provider_tile_data = tile_data["providers"][texture_id]
            new_provider.width = provider_tile_data["width"]
            new_provider.height = provider_tile_data["height"]

            new_provider.chars = provider["chars"]
            new_provider.baseline = provider["ascent"]

            new_providers.append(new_provider)

    return new_providers

def load_tile_data(mc_version: str) -> dict:
    filename = "resources/" + mc_version + ".toml"
    with open(filename, "r") as file:
        return tomllib.loads(file.read())

def build_tileset(tileset_data: dict, providers: list[Provider]) -> (Image, str):
    tile_width = tileset_data["tile_width"]
    tile_height = tileset_data["tile_height"]
    tile_baseline = tileset_data["tile_baseline"]
    tileset_width = tileset_data["tileset_width"]

    tileset = Image.new("RGBA", (tileset_width, tile_height), color=(255, 0, 0, 0))
    glyphs: str = ""
    tileset_x = 0

    for provider in providers:
        char_height = provider.height
        char_width = provider.width
        char_baseline = provider.baseline
        tile_height_offset = tile_baseline - char_baseline

        font_img = Image.open(io.BytesIO(provider.file))
        font_x = font_y = 0
        for chars in provider.chars:  # "abcdefghij"
            for char in chars:  # "a"
                if char != "\x00":
                    char_img = font_img.crop((font_x, font_y, font_x + char_width, font_y + char_height))
                    tileset.paste(char_img, (tileset_x, tile_height_offset))
                    glyphs += char

                    tileset_x += tile_width
                font_x += char_width
            font_x = 0
            font_y += char_height


    return tileset, glyphs


def convert_to_pixel_font_converter_batch(tileset: Image, glyphs: str, tileset_data: dict):
    with open("resources/pixel_font_converter_settings.json") as settings_file:
        settings = json.load(settings_file)

    settings["glyph-width"] = tileset_data["tile_width"]
    settings["glyph-height"] = tileset_data["tile_height"]
    settings["glyph-baseline"] = tileset_data["tile_baseline"]

    settings["in-glyphs"] = [glyphs]

    with open("out/Minecraft Seven.json", "w") as settings_output_file:
        json.dump(settings, settings_output_file)

    tileset.save("out/Minecraft Seven.png")


def build_as_pixel_font_converter_batch(jar_path: str, mc_version: str):
    tile_data = load_tile_data(mc_version)
    providers = get_assets(jar_path, tile_data)
    for provider in providers:
        print(provider.id)
    tileset, glyphs = build_tileset(tile_data["tileset"], providers)
    convert_to_pixel_font_converter_batch(tileset, glyphs, tile_data["tileset"])