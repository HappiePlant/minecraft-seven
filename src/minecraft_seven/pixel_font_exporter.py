import json

from PIL import Image

from minecraft_seven.builder import OutputDimensions


def export_to_pixel_font_converter_batch(
    tileset: Image, glyphs: str, out: OutputDimensions
):
    with open("resources/pixel_font_converter_settings.json") as settings_file:
        settings = json.load(settings_file)

    settings["glyph-width"] = out.tile_width
    settings["glyph-height"] = out.tile_height
    settings["glyph-baseline"] = out.tile_baseline

    settings["in-glyphs"] = [glyphs]

    with open("out/Minecraft Seven.json", "w") as settings_output_file:
        json.dump(settings, settings_output_file)

    tileset.save("out/Minecraft Seven.png")
