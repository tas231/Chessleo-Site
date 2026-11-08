#!/bin/sh
# Builds the WebP images the pages load from the PNG/JPG originals in assets/.
# Run it after replacing or adding a screenshot, then commit the .webp files too.
# Needs cwebp (brew install webp). The originals stay in assets/ as the source.
set -eu
cd "$(dirname "$0")/../assets"

# Screenshots: full size, they fill the mockup frames on retina screens.
for base in screen-zaubertisch screen-design-edel screen-design-bunt screen-school-prolog \
            screen-school-bishop screen-school-italian screen-diplom; do
  for lang in de en es fr tr zh; do
    cwebp -quiet -q 82 -m 6 -sharp_yuv "$base-$lang.png" -o "$base-$lang.webp"
  done
done
cwebp -quiet -q 82 -m 6 -sharp_yuv screen-freeplay.png -o screen-freeplay.webp

# Logo is shown 148 px wide, avatars 96 px: three times that is enough for every screen.
cwebp -quiet -q 85 -m 6 -alpha_q 90 -resize 444 0 logo-artistic-transparent.png -o logo-artistic-transparent.webp
for name in avatar_max avatar_lina avatar_theo avatar_titan; do
  cwebp -quiet -q 82 -m 6 -resize 288 0 "$name.jpg" -o "$name.webp"
done
for name in pieces-kawaii pieces-asia pieces-fantasy; do
  cwebp -quiet -q 82 -m 6 "$name.jpg" -o "$name.webp"
done

echo "WebP images rebuilt."
