# Card logos

Each card on the site shows a logo from this folder when the file exists, and a short text badge
otherwise. Use the official logo file from each organisation's own site or media kit, unaltered,
saved as a square PNG (at least 128 by 128 pixels) with the name below. Then commit it.

Check each organisation's brand rules first: some only allow their logo in specific cases, and some
(IEEE among them) restrict use of the logo by individuals.

| Card | File name |
|---|---|
| IET Software | `iet.png` |
| IEEE CCWC 2027 | `ieee-ccwc.png` |
| ISASF 2026 | `isasf.png` |
| IIPEM 2026 | `iipem.png` |
| Preprints | `preprints.png` |
| HackerNoon | `hackernoon.png` |
| Snowflake Builders Blog | `snowflake.png` |
| DEV Community | `dev.png` |
| DZone | `dzone.png` |
| TAIMMA 2027 | `taimma.png` |
| Conf42 Chaos Engineering 2026 | `conf42.png` |
| Earlier talks | `talks.png` |
| IEEE Access | `ieee-access.png` |
| IEEE IT Professional | `ieee-itpro.png` |
| Hackathons | `hackathons.png` |
| IEEE and IET | `memberships.png` |
| UK Registered Design | `uk-design.png` |

After adding files, run `python3 scripts/build_static.py` so the page's static copy shows them too.
