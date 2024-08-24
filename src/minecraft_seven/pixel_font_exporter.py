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

    show_done_msg()


def show_done_msg():
    print(f"""
Done!
    
1. Go to {link("https://yal.cc/r/20/pixelfont/", "[🔗 Pixel Font Converter]")}
2. Click `Menu` on the upper left and select `Batch process`
3. Navigate to the `out` folder in this repo and select both the `png` and `json` file. (by holding `Ctrl`)
4. Install the ttf in the downloaded zip!
    """)


def link(uri: str, label: str = None):
    if label is None:
        label = uri
    parameters = ""

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"

    return escape_mask.format(parameters, uri, label)
