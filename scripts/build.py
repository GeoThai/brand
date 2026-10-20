"""Builds every GeoThai logo file from the typeface, so the marks can be made again exactly.

The symbol is the G of Bai Jamjuree SemiBold (the wordmark's typeface) with its lower outer curve
drawn out into the tip of a location pin. Run: python3 scripts/build.py
Needs fontTools; PNG and ICO output also needs cairosvg and Pillow.
"""
import io
import json
import os

from fontTools.pens.basePen import decomposeQuadraticSegment
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

ROOT = os.path.join(os.path.dirname(__file__), '..')
FONT = os.path.join(ROOT, 'fonts', 'BaiJamjuree-SemiBold.ttf')

LATERITE = '#B5452A'
LATERITE_LIGHT = '#EE8461'
BLACK = '#000000'
WHITE = '#FFFFFF'

# Symbol geometry in font units (y up). The G spans y -8..708; the pin tip sits below it.
TIP_DEPTH = 240
TIP_DEPTH_SMALL = 300  # favicon cut: a longer tip keeps the pin readable at 16 px
HANDLE_SIDE, HANDLE_TIP = 0.45, 0.55
G_TOP = 708
CAP = 700

_font = TTFont(FONT)
_glyphs = _font.getGlyphSet()
_cmap = _font.getBestCmap()
_hmtx = _font['hmtx']


def num(n):
    return f'{n:.2f}'.rstrip('0').rstrip('.')


def _segments(glyph):
    pen = RecordingPen()
    _glyphs[glyph].draw(pen)
    return pen.value


def _path(segments, X, Y):
    d = []
    for op, args in segments:
        if op == 'moveTo':
            d.append(f'M{X(args[0][0])} {Y(args[0][1])}')
        elif op == 'lineTo':
            d.append(f'L{X(args[0][0])} {Y(args[0][1])}')
        elif op == 'qCurveTo':
            for c, p in decomposeQuadraticSegment(args):
                d.append(f'Q{X(c[0])} {Y(c[1])} {X(p[0])} {Y(p[1])}')
        elif op == 'curveTo':
            (a, b, p) = args
            d.append(f'C{X(a[0])} {Y(a[1])} {X(b[0])} {Y(b[1])} {X(p[0])} {Y(p[1])}')
        elif op == 'closePath':
            d.append('Z')
    return ''.join(d)


def pin_segments(tip_depth=TIP_DEPTH):
    """The G outline with its lower outer curve replaced by two smooth sides meeting at the tip."""
    segs = _segments('G')
    cut = next(i for i, (op, a) in enumerate(segs) if op == 'lineTo' and a[0] == (659, 241))
    left = segs[0][1][0]
    right = segs[cut][1][0]
    tip = ((left[0] + right[0]) / 2, -tip_depth)
    hr = (right[1] - tip[1]) * HANDLE_SIDE
    hl = (left[1] - tip[1]) * HANDLE_SIDE
    side_r = (tip[0] + (right[0] - tip[0]) * HANDLE_TIP, tip[1] + (right[1] - tip[1]) * HANDLE_TIP * 0.55)
    side_l = (tip[0] + (left[0] - tip[0]) * HANDLE_TIP, tip[1] + (left[1] - tip[1]) * HANDLE_TIP * 0.55)
    return segs[:cut + 1] + [
        ('curveTo', ((right[0], right[1] - hr), side_r, tip)),
        ('curveTo', (side_l, (left[0], left[1] - hl), left)),
        ('closePath', ()),
    ], tip


PIN_X0, PIN_X1 = 48, 659  # the G's outer left and right sides


def pin(scale, left, top, tip_depth=TIP_DEPTH):
    """Pin path; (left, top) is the top-left of its bounding box in px."""
    segs, _ = pin_segments(tip_depth)
    return _path(segs, lambda x: num(left + (x - PIN_X0) * scale), lambda y: num(top + (G_TOP - y) * scale))


def pin_size(scale, tip_depth=TIP_DEPTH):
    return (PIN_X1 - PIN_X0) * scale, (G_TOP + tip_depth) * scale


def wordmark(scale, left, baseline, text='GeoThai'):
    """Wordmark path and its advance width in px. Outline starts at the first glyph's left side bearing."""
    d, x = [], 0
    for ch in text:
        g = _cmap[ord(ch)]
        ox = x
        d.append(_path(_segments(g), lambda v, ox=ox: num(left + (ox + v) * scale), lambda v: num(baseline - v * scale)))
        x += _hmtx[g][0]
    first_lsb = _hmtx[_cmap[ord(text[0])]][1]
    last = _cmap[ord(text[-1])]
    ink_width = x - first_lsb - (_hmtx[last][0] - _glyph_xmax(last))
    return ''.join(d), first_lsb * scale, ink_width * scale


def _glyph_xmax(glyph):
    from fontTools.pens.boundsPen import BoundsPen
    pen = BoundsPen(_glyphs)
    _glyphs[glyph].draw(pen)
    return pen.bounds[2]


def svg(w, h, body, title='GeoThai'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {num(w)} {num(h)}" width="{num(w)}" '
            f'height="{num(h)}" role="img"><title>{title}</title>{body}</svg>\n')


def symbol_svg(color, size=256, pad=22, tip_depth=TIP_DEPTH):
    w, h = pin_size(1, tip_depth)
    scale = (size - 2 * pad) / h
    pw = w * scale
    return svg(size, size, f'<path d="{pin(scale, (size - pw) / 2, pad, tip_depth)}" fill="{color}"/>', 'GeoThai')


# Lockups: the cap height H sets every size. The symbol's G is 1.3 H tall and sits on the cap
# middle; the gap to the wordmark is 0.6 H; clear space around a lockup is 0.5 H.
SYMBOL_G = 1.3
GAP = 0.6
CLEAR = 0.5


def horizontal_svg(sym_color, word_color, H=100):
    s_word = H / CAP
    s_sym = SYMBOL_G * H / G_TOP
    sw, sh = pin_size(s_sym)
    g_h = G_TOP * s_sym
    pad = CLEAR * H
    # the symbol's G is centred on the cap height; the tip hangs below
    sym_top = pad + max(0, (g_h - H) / 2)
    baseline = sym_top + (g_h + H) / 2
    word_d, lsb, word_w = wordmark(s_word, 0, baseline)
    x_word = pad + sw + GAP * H - lsb
    word_d, _, _ = wordmark(s_word, x_word, baseline)
    w = pad + sw + GAP * H + word_w + pad
    h = max(sym_top + sh, baseline) + pad
    body = (f'<path d="{pin(s_sym, pad, sym_top)}" fill="{sym_color}"/>'
            f'<path d="{word_d}" fill="{word_color}"/>')
    return svg(w, h, body)


def stacked_svg(sym_color, word_color, H=100):
    s_word = H / CAP
    s_sym = 2.4 * H / G_TOP
    sw, sh = pin_size(s_sym)
    pad = CLEAR * H
    _, lsb, word_w = wordmark(s_word, 0, 0)
    w = max(sw, word_w) + 2 * pad
    sym_left = (w - sw) / 2
    baseline = pad + sh + 0.55 * H + H
    word_d, _, _ = wordmark(s_word, (w - word_w) / 2 - lsb, baseline)
    h = baseline + pad
    body = (f'<path d="{pin(s_sym, sym_left, pad)}" fill="{sym_color}"/>'
            f'<path d="{word_d}" fill="{word_color}"/>')
    return svg(w, h, body)


def wordmark_svg(color, H=100):
    s_word = H / CAP
    pad = CLEAR * H
    _, lsb, word_w = wordmark(s_word, 0, 0)
    word_d, _, _ = wordmark(s_word, pad - lsb, pad + H)
    return svg(word_w + 2 * pad, H + 2 * pad, f'<path d="{word_d}" fill="{color}"/>')


VERSIONS = {
    # name: (symbol colour, wordmark colour)
    'color': (LATERITE, BLACK),
    'color-on-dark': (LATERITE_LIGHT, WHITE),
    'black': (BLACK, BLACK),
    'white': (WHITE, WHITE),
}


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(text)
    return full


def build_svgs():
    for version, (sym, word) in VERSIONS.items():
        write(f'logo/symbol/geothai-symbol-{version}.svg', symbol_svg(sym))
        write(f'logo/horizontal/geothai-horizontal-{version}.svg', horizontal_svg(sym, word))
        write(f'logo/stacked/geothai-stacked-{version}.svg', stacked_svg(sym, word))
        write(f'logo/wordmark/geothai-wordmark-{version}.svg', wordmark_svg(word))
    write('logo/symbol/geothai-symbol-small.svg', symbol_svg(LATERITE, tip_depth=TIP_DEPTH_SMALL, pad=10))


def build_icons():
    import cairosvg
    from PIL import Image

    def png(svg_text, px):
        return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_text.encode(), output_width=px, output_height=px)))

    small = symbol_svg(LATERITE, tip_depth=TIP_DEPTH_SMALL, pad=10)
    write('icons/favicon.svg', small)
    os.makedirs(os.path.join(ROOT, 'icons'), exist_ok=True)
    frames = [png(small, px).convert('RGBA') for px in (16, 32, 48)]
    frames[0].save(os.path.join(ROOT, 'icons', 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)], append_images=frames[1:])
    for px in (16, 32, 48):
        png(small, px).save(os.path.join(ROOT, 'icons', f'favicon-{px}.png'))

    def tile(bg, fg, size=1024, mark=0.62, radius=0.22):
        w, h = pin_size(1)
        scale = size * mark / h
        pw = w * scale
        top = (size - h * scale) / 2 - size * 0.01
        r = size * radius
        body = (f'<rect width="{size}" height="{size}" rx="{num(r)}" fill="{bg}"/>'
                f'<path d="{pin(scale, (size - pw) / 2, top)}" fill="{fg}"/>')
        return svg(size, size, body)

    def full(bg, fg, size=1024, mark=0.56):
        w, h = pin_size(1)
        scale = size * mark / h
        pw = w * scale
        top = (size - h * scale) / 2 - size * 0.01
        return svg(size, size, f'<rect width="{size}" height="{size}" fill="{bg}"/>'
                               f'<path d="{pin(scale, (size - pw) / 2, top)}" fill="{fg}"/>')

    app = write('icons/app-icon.svg', tile(LATERITE, WHITE))
    avatar = write('icons/avatar.svg', full(LATERITE, WHITE))
    maskable = full(LATERITE, WHITE, mark=0.46)
    for name, text, sizes in (('apple-touch-icon', open(app).read(), (180,)), ('icon', open(app).read(), (192, 512)),
                              ('maskable', maskable, (512,)), ('avatar', open(avatar).read(), (500, 1024))):
        for px in sizes:
            suffix = '' if name == 'apple-touch-icon' else f'-{px}'
            png(text, px).save(os.path.join(ROOT, 'icons', f'{name}{suffix}.png'))

    write('icons/site.webmanifest', json.dumps({
        'name': 'GeoThai', 'short_name': 'GeoThai', 'theme_color': LATERITE, 'background_color': WHITE,
        'display': 'standalone',
        'icons': [
            {'src': '/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
            {'src': '/maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
    }, indent=2) + '\n')
    write('icons/head-snippet.html', (
        '<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '<link rel="manifest" href="/site.webmanifest">\n'
        f'<meta name="theme-color" content="{LATERITE}">\n'))


if __name__ == '__main__':
    build_svgs()
    build_icons()
    print('built logo/ and icons/')
