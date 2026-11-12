#!/usr/bin/env python3
"""Builds the six press kits in assets/ (one ZIP per language).

Each kit holds the factsheet of its language, the founder story, screenshots of the app in that
language only, the character artworks, logos, key visuals and (German, English) the printable
diploma. Screenshots go in as high-quality JPEG (PNG originals are 3-7 MB each), transparent
artworks and logos stay as they are.

Sources:
  - this repository's assets/ (factsheets ChessLeo_Factsheet_*.txt, localized website screenshots)
  - the app repository's Pressekit/ folder (German in-game screenshots, artworks, logos, banner,
    diplomas, founder stories, free-play frames from the gameplay videos)

The ZIPs are reproducible: fixed file dates and the same JPEG settings, so running the script
again without changed sources writes byte-identical files and git sees no change. Every new kit
version still adds its size to the repository, so rebuild only when the content really changed.

Usage: python3 tools/build_presskits.py           (needs Pillow, e.g. the app repo's venv)
       python3 tools/build_presskits.py --check   (exit 1 if a ZIP is out of date)
"""

import io
import sys
import zipfile
from pathlib import Path

from PIL import Image

SITE = Path(__file__).resolve().parent.parent
ASSETS = SITE / "assets"
PRESSKIT = Path("/Users/tobias/Documents/MacDev/ChessLeo/Pressekit")
DATE = (2026, 11, 12, 0, 0, 0)
STAND = "12.11.2026"

# In-game screenshots that must not appear before the matching release.
NOT_YET_RELEASED = {"13_Sticker_Album_Kostuemfest.png"}  # sticker album ships with 1.0.5

KITS = {
    "de": ("ChessLeo_Pressekit.zip", "ChessLeo_Factsheet_Presse.txt"),
    "en": ("ChessLeo_PressKit_EN.zip", "ChessLeo_Factsheet_EN.txt"),
    "fr": ("ChessLeo_DossierPresse_FR.zip", "ChessLeo_Factsheet_FR.txt"),
    "es": ("ChessLeo_KitPrensa_ES.zip", "ChessLeo_Factsheet_ES.txt"),
    "tr": ("ChessLeo_BasinKiti_TR.zip", "ChessLeo_Factsheet_TR.txt"),
    "zh": ("ChessLeo_PressKit_ZH.zip", "ChessLeo_Factsheet_ZH.txt"),
}
LANGUAGE_NAME = {"de": "German", "en": "English", "fr": "French", "es": "Spanish", "tr": "Turkish",
                 "zh": "Simplified Chinese"}

# Localized website screenshots: (asset base, file name in the kit). German kit uses the German
# in-game set instead and adds only the lessons and the Classic design from this list.
LOCALIZED = [
    ("screen-zaubertisch", "Home_Magic_Table"),
    ("screen-design-edel", "Home_Classic_Elegant_Light"),
    ("screen-design-edel-dark", "Home_Classic_Elegant_Dark"),
    ("screen-design-bunt", "Home_Classic_Colorful"),
    ("screen-school-prolog", "Lesson_Prologue_What_Is_Chess"),
    ("screen-school-bishop", "Lesson_Grade1_The_Bishop"),
    ("screen-school-italian", "Lesson_Grade3_Italian_Game"),
    ("screen-diplom", "Master_Diploma"),
]
GERMAN_EXTRAS = [
    ("screen-design-bunt", "17_Startbildschirm_Klassisch_Bunt"),
    ("screen-school-prolog", "18_Prolog_Was_ist_Schach"),
    ("screen-school-bishop", "19_Lektion_Der_Laeufer"),
    ("screen-school-italian", "20_Lektion_Italienische_Partie"),
]

FOLDERS = {
    "de": ["00_Info", "01_Screenshots_iPad", "02_Charaktere", "03_Logos", "04_Key_Visuals", "05_Meister_Diplom"],
    "other": ["00_Info", "01_Screenshots", "02_Characters", "03_Logos", "04_Key_Visuals", "05_Master_Diploma"],
}


def jpeg_bytes(path):
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        background = Image.new("RGB", im.size, (0, 0, 0))
        background.paste(im, mask=im.split()[-1])
        im = background
    else:
        im = im.convert("RGB")
    out = io.BytesIO()
    im.save(out, "JPEG", quality=90, subsampling=0, optimize=True)
    return out.getvalue()


def readme(lang, folders, screenshot_count):
    if lang == "de":
        return f"""CHESSLEO ACADEMY – PRESSE-KIT (DEUTSCH)
Stand: {STAND}

ORDNER
{folders[0]}            Factsheet, Entstehungsgeschichte, diese Datei
{folders[1]}  {screenshot_count} Screenshots der deutschen App (iPad, JPEG)
{folders[2]}       Coach Vogel, Leo, Lina, Opa Theo und Titan (PNG freigestellt bzw. JPG)
{folders[3]}            App-Icon 1024 px, Logo transparent (PNG), Druck-Logo (SVG, JPEG)
{folders[4]}      Key Visual ohne Text, Charakter-Banner
{folders[5]}   Druckvorlage des Meister-Diploms

Einzelne Bilder in voller Auflösung gibt es auch auf https://chessleo.de/presse.html

NUTZUNG
Alle Bilder und Texte dürfen für die redaktionelle Berichterstattung über
ChessLeo Academy honorarfrei verwendet werden.

KONTAKT
presse@chessleo.de · https://chessleo.de/presse.html
"""
    diploma = (f"{folders[5]}  Printable Master Diploma\n" if lang == "en" else "")
    return f"""CHESSLEO ACADEMY – PRESS KIT ({LANGUAGE_NAME[lang].upper()})
As of {STAND}

FOLDERS
{folders[0]}          Factsheet, founder story, this file
{folders[1]}   {screenshot_count} screenshots of the app in {LANGUAGE_NAME[lang]}
{folders[2]}    Coach Bird, Leo, Lina, Grandpa Theo and Titan (transparent PNG or JPG)
{folders[3]}          App icon 1024 px, transparent logo (PNG), print logo (SVG, JPEG)
{folders[4]}    Key visual without text, character banner
{diploma}
USAGE
All images and texts may be used free of charge for editorial coverage of
ChessLeo Academy.

CONTACT
presse@chessleo.de · https://chessleo.de/en/press.html
"""


def kit_entries(lang):
    """Returns [(path in zip, bytes)] for one language."""
    folders = FOLDERS["de" if lang == "de" else "other"]
    entries = []
    factsheet = KITS[lang][1]
    shots = []
    if lang == "de":
        for png in sorted((PRESSKIT / "01_Screenshots_InGame_Original").glob("*.png")):
            if png.name not in NOT_YET_RELEASED:
                shots.append((png.stem + ".jpg", jpeg_bytes(png)))
        for base, name in GERMAN_EXTRAS:
            shots.append((name + ".jpg", jpeg_bytes(ASSETS / f"{base}-de.png")))
        shots.append(("21_Partie_gegen_Leo.jpg", jpeg_bytes(PRESSKIT / "06_Freies_Spiel_lokalisiert/freeplay_de.png")))
    else:
        for number, (base, name) in enumerate(LOCALIZED, start=1):
            shots.append((f"{number:02d}_{name}.jpg", jpeg_bytes(ASSETS / f"{base}-{lang}.png")))
        shots.append((f"{len(LOCALIZED) + 1:02d}_Free_Play_against_Leo.jpg",
                      jpeg_bytes(PRESSKIT / f"06_Freies_Spiel_lokalisiert/freeplay_{lang}.png")))

    entries.append((f"{folders[0]}/{'LIESMICH' if lang == 'de' else 'README'}.txt",
                    readme(lang, folders, len(shots)).encode("utf-8")))
    entries.append((f"{folders[0]}/{factsheet.replace('Presse', 'DE')}", (ASSETS / factsheet).read_bytes()))
    story = ("Die_wahre_Entstehungsgeschichte_Gruenderstory.txt" if lang == "de"
             else "The_True_Origin_Story_Founder_Story.txt")
    entries.append((f"{folders[0]}/{story}", (PRESSKIT / "00_Factsheet_Info" / story).read_bytes()))
    entries += [(f"{folders[1]}/{name}", data) for name, data in shots]
    for folder, target in [("02_Charaktere_Artworks", folders[2]), ("03_Logos_Icons", folders[3])]:
        for f in sorted((PRESSKIT / folder).iterdir()):
            if f.is_file() and not f.name.startswith("."):
                entries.append((f"{target}/{f.name}", f.read_bytes()))
    for f in sorted((PRESSKIT / "04_Key_Visuals_Banner").iterdir()):
        if f.is_file() and not f.name.startswith("."):
            entries.append((f"{folders[4]}/{f.name}", f.read_bytes()))
    if lang == "de":
        entries.append((f"{folders[5]}/ChessLeo_Meister_Diplom_Druckvorlage_DE.png",
                        (PRESSKIT / "05_Meister_Diplom/ChessLeo_Meister_Diplom_Druckvorlage_DE.png").read_bytes()))
    elif lang == "en":
        entries.append((f"{folders[5]}/ChessLeo_Master_Diploma_Printable_EN.png",
                        (PRESSKIT / "05_Meister_Diplom/ChessLeo_Master_Diploma_Printable_EN.png").read_bytes()))
    return entries


def zip_bytes(entries):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=DATE)
            info.external_attr = 0o644 << 16
            compressed = name.endswith((".txt", ".svg"))
            info.compress_type = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
            z.writestr(info, data, compresslevel=9 if compressed else None)
    return out.getvalue()


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for lang, (zip_name, _) in KITS.items():
        data = zip_bytes(kit_entries(lang))
        path = ASSETS / zip_name
        old = path.read_bytes() if path.exists() else None
        state = "unchanged" if old == data else "updated"
        if old != data:
            stale.append(zip_name)
            if not check:
                path.write_bytes(data)
        print(f"{lang}: {zip_name} {len(data) / 1e6:.1f} MB ({state})")
    if check and stale:
        print("out of date:", ", ".join(stale))
        sys.exit(1)


if __name__ == "__main__":
    main()
