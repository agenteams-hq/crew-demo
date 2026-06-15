# Tileset licensing

## Tiny Town (used)
- **Pack:** Kenney - Tiny Town (v1.1)
- **Source:** https://kenney.nl/assets/tiny-town
- **Direct download:** https://kenney.nl/media/pages/assets/tiny-town/a415fbeb49-1735736916/kenney_tiny-town.zip
- **License:** Creative Commons Zero (CC0 1.0) - https://creativecommons.org/publicdomain/zero/1.0/
- **Attribution:** NOT required. Free for personal, educational and commercial use. Crediting Kenney / www.kenney.nl is appreciated but optional.
- **Format:** 16x16 px tiles, packed atlas `tiny-town/Tilemap/tilemap_packed.png` (192x176 = 12 cols x 11 rows = 132 tiles).
- **Used for:** Full-frame tile-based cozy meadow in `mocks/crew-scene.html` (grass variants, trees, bushes, flowers, mushrooms, dirt path, cobble).

We render `tilemap_packed.png` directly tile-by-tile with nearest-neighbor scaling. No redistribution restriction (CC0), so the atlas is committed into this repo as-is.

## Notes for the CEO / paid upgrade path
- Tiny Town (CC0) is the safe, commit-able prototype tileset and is genuinely cozy/Sprout-Lands-adjacent.
- If we want an even closer "Sprout Lands" look later, **Cup Nooble - Sprout Lands** (https://cupnooble.itch.io/sprout-lands-asset-pack) is free but its license forbids redistribution even when modified, so it CANNOT be committed into a public repo without legal review. It would need to be loaded from a private/licensed location, or we buy a redistributable commercial license.
- CraftPix "Grassland Top Down Tileset" is a paid pack with broader transitions/auto-tiling if we want to invest.
