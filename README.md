# GeoThai brand

The GeoThai logo, colors, icons and usage rules, built from one typeface by one script.

[👉 Overview](./docs/overview.png) · [Presentation](./docs/presentation.md)

## Features

- One symbol: the G of the wordmark's typeface, with its lower curve drawn out into the tip of a location pin. One letter says the name and the place
- Four lockups in black and white, as outlined SVG
- A small-size symbol with a longer tip for 16 px favicons
- Web and app icons: favicon, Apple touch icon, PWA icons, maskable icon, social avatar, web manifest
- Every file made again from the font by [`scripts/build.py`](./scripts/build.py)

## The Logo

| Version    | Use                                                | Files                                   |
| ---------- | -------------------------------------------------- | --------------------------------------- |
| Horizontal | The default: headers, README, slides               | [`logo/horizontal/`](./logo/horizontal) |
| Stacked    | Square or narrow spaces                            | [`logo/stacked/`](./logo/stacked)       |
| Symbol     | Avatars, app icons, favicons, small spaces         | [`logo/symbol/`](./logo/symbol)         |
| Wordmark   | Text-only contexts, after the symbol already shows | [`logo/wordmark/`](./logo/wordmark)     |

Each version comes in two colors:

| File suffix | Logo  | Background                                |
| ----------- | ----- | ----------------------------------------- |
| `-black`    | Black | White, light backgrounds, one-color print |
| `-white`    | White | Black, dark UI, photos with a calm area   |

## Clear Space

Keep a clear zone of half the wordmark's cap height (0.5 H) on every side. The SVG files already include this zone. The zone scales with the logo, so never use a fixed distance.

In the horizontal lockup, the symbol's G is 1.3 H tall and centered on the caps, and the gap to the wordmark is 0.6 H. Do not change these sizes.

## Minimum Size

| Version    | Screen                                                                                                                                 |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Horizontal | 120 px wide                                                                                                                            |
| Stacked    | 64 px wide                                                                                                                             |
| Symbol     | 24 px tall. Below 24 px, use [`logo/symbol/geothai-symbol-small.svg`](./logo/symbol/geothai-symbol-small.svg), which has a longer tip. |

## Color

| Name  | HEX       | RGB         | CMYK      | Use                       |
| ----- | --------- | ----------- | --------- | ------------------------- |
| Black | `#000000` | 0 0 0       | 0 0 0 100 | Logo, text, app icons     |
| White | `#FFFFFF` | 255 255 255 | 0 0 0 0   | Backgrounds, logo on dark |

The brand has no accent color. The shape of the G-pin carries the identity. Black on white is 21 : 1.

A color for the brand was tested and dropped: the red-brown candidates sat close to the error red of developer tools, to Thai brands and to a common AI default.

## Typography

- Wordmark and headings: [Bai Jamjuree](https://github.com/cadsondemak/Bai-Jamjuree) SemiBold by Cadson Demak. It has Thai and Latin in one family. License: SIL Open Font License, in [`fonts/OFL.txt`](./fonts/OFL.txt).
- Body text: Bai Jamjuree Regular, or the system sans-serif.
- The wordmark in the logo files is outlined. Do not retype it.

## Icons

[`icons/`](./icons) holds the web and app set:

| File                                                                       | Use                                                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `favicon.ico`, `favicon.svg`, `favicon-16/32/48.png`                       | Browser tabs                                                                   |
| `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `maskable-512.png` | Home screens and PWA                                                           |
| `avatar.svg`, `avatar-500.png`, `avatar-1024.png`                          | GitHub org, npm, social profiles (square, crops to a circle). White G on black |
| `app-icon.svg`                                                             | App icon master                                                                |
| `site.webmanifest`, `head-snippet.html`                                    | Copy into a website                                                            |

## Do Not

- Stretch, squash, rotate or slant the logo.
- Recolor it. Use black or white only.
- Add shadows, outlines, gradients or effects.
- Move, resize or swap the parts of a lockup.
- Put it on a busy photo without a calm area or a solid panel.
- Use the old logo with the map of Thailand.

## Rebuild

Every logo and icon file is made from the typeface by one script. To change a size or a color, edit [`scripts/build.py`](./scripts/build.py) and run it:

```bash
pip install fonttools cairosvg pillow
python3 scripts/build.py
```

## Why?

The old GeoThai logo was a map of Thailand in blue. Most map and geodata brands use a map, a globe or a pin in blue, so it looked like all of them. It also had no link to the name. The new symbol starts from the letter G of the wordmark and adds the pin. It is black and white, so it sits next to any product without a clash.

## License

The GeoThai name and logo: all rights reserved © 2026 [Pongsakorn Thipayanate](https://github.com/pyyupsk). Bai Jamjuree: SIL Open Font License 1.1.
