import io
import tomllib
from zipfile import ZipFile
import json
from PIL import Image, ImageDraw


type MinecraftClientJar = ZipFile


class Provider:
    id: str
    file: bytes
    width: int
    height: int
    baseline: int
    chars: list[str]


class OutputDimensions:
    tile_width: int
    tile_height: int
    tile_baseline: int
    space_width: int
    tileset_width: int


def get_space_width(jar: MinecraftClientJar):
    space_data: dict = json.loads(jar.read("assets/minecraft/font/include/space.json"))
    return space_data["providers"][0]["advances"][" "]


def get_font_data(jar: MinecraftClientJar):
    return json.loads(jar.read("assets/minecraft/font/include/default.json"))


def get_assets(
    jar_path: str, dimensions: dict
) -> tuple[list[Provider], OutputDimensions]:
    out = OutputDimensions()
    out.tileset_width = dimensions["output"]["tileset_width"]

    with ZipFile(jar_path, "r") as jar:
        font_data = get_font_data(jar)
        providers: list[dict] = font_data["providers"]
        new_providers: list[Provider] = []
        out.tile_width = 0
        out.tile_height = 0
        out.tile_baseline = 0

        for provider in providers:
            provider_dimensions = dimensions["providers"][provider["file"]]
            new_provider = map_provider_json_to_class(
                jar, provider, provider_dimensions
            )

            if new_provider.width > out.tile_width:
                out.tile_width = new_provider.width
            if new_provider.height > out.tile_height:
                out.tile_height = new_provider.height
                out.tile_baseline = new_provider.baseline

            new_providers.append(new_provider)

        out.space_width = get_space_width(jar)

    return new_providers, out


def map_provider_json_to_class(jar: MinecraftClientJar, provider, provider_dimensions):
    new_provider: Provider = Provider()
    texture_id: str = provider["file"]

    new_provider.id = texture_id
    texture_name = texture_id.replace("minecraft:", "assets/minecraft/textures/")
    new_provider.file = jar.read(texture_name)
    new_provider.width = provider_dimensions["width"]
    new_provider.height = provider_dimensions["height"]
    new_provider.chars = provider["chars"]
    new_provider.baseline = provider["ascent"]
    return new_provider


def load_dimensions(mc_version: str) -> dict:
    filename = "resources/" + mc_version + ".toml"
    with open(filename, "r") as file:
        return tomllib.loads(file.read())


def create_space_tile(width: int, height: int, space_width: int) -> Image:
    tile = Image.new("RGBA", (width, height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(tile)
    draw.rectangle((0, 0, space_width - 2, height), fill="white")
    return tile


def build_tileset(
    providers: list[Provider], out: OutputDimensions
) -> tuple[Image, str]:
    tileset = Image.new(
        "RGBA", (out.tileset_width, out.tile_height), color=(255, 0, 0, 0)
    )
    glyphs: str = ""
    tileset_x = 0

    for provider in providers:
        char_height = provider.height
        char_width = provider.width
        char_baseline = provider.baseline
        tile_height_offset = out.tile_baseline - char_baseline

        font_img = Image.open(io.BytesIO(provider.file))
        font_x = font_y = 0
        for chars in provider.chars:  # "abcdefghij"
            for char in chars:  # "a"
                if char != "\x00":
                    print(char)
                    if char != " ":
                        char_img = font_img.crop(
                            (font_x, font_y, font_x + char_width, font_y + char_height)
                        )
                    else:
                        char_img = create_space_tile(
                            char_width, char_height, out.space_width
                        )
                    tileset.paste(char_img, (tileset_x, tile_height_offset))
                    glyphs += char

                    tileset_x += out.tile_width
                font_x += char_width
            font_x = 0
            font_y += char_height

    return tileset, glyphs


def build_font_assets(
    jar_path: str, mc_version: str
) -> tuple[Image, str, OutputDimensions]:
    dimensions = load_dimensions(mc_version)
    providers, output_dimensions = get_assets(jar_path, dimensions)
    for provider in providers:
        print(provider.id)

    tileset, glyphs = build_tileset(providers, output_dimensions)

    return tileset, glyphs, output_dimensions
