# Minecraft Seven Builder

Tool to build the minecraft font files into a format for [Pixel Font Converter](https://yellowafterlife.itch.io/pixelfont)

This project aims to be 100% faithful to the original Minecraft font by providing all glyphs and correct spacing.

## Build steps
### Using [`uv`](https://docs.astral.sh/uv/)

1. Clone this repo
2. Run `uv run src/minecraft_seven/__init__.py`
3. Open [Pixel Font Converter](https://yal.cc/r/20/pixelfont/)
4. Click `Menu` in the top right and select `Batch process`
5. Navigate to the `out` folder in this repo and select both the `png` and `json` file. (by holding <kbd>Ctrl</kbd>)
6. Install the ttf in the downloaded zip!

## Known issues
- The font doesn't look right when used in LibreSprite

## Planned features
- [x] Build the Minecraft font files into a format for Pixel Font Converter
- [ ] Options for generating the enchanting table or illager font.