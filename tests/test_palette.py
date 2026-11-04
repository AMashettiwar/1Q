"""WCAG contrast checks for the wardrobe palette."""
import pytest

from oneq import ui


def _lum(hexc):
    h = hexc.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


@pytest.mark.parametrize("theme", ["ivory", "ink"])
def test_text_contrast(theme):
    t = ui.THEMES[theme]
    for bg in (t["bg"], t["surface"], t["surface2"]):
        assert ratio(t["ink"], bg) >= 7
        assert ratio(t["muted"], bg) >= 4.5
        assert ratio(t["on_primary"], t["primary"]) >= 4.5


@pytest.mark.parametrize("theme", ["ivory", "ink"])
@pytest.mark.parametrize("name", list(ui.PALETTE))
def test_tones_readable_as_text(theme, name):
    t = ui.THEMES[theme]
    assert ratio(ui.tone(name, theme), t["surface"]) >= 4.5, (name, theme)
    assert ratio(ui.tone(name, theme), t["surface2"]) >= 4.5, (name, theme)


@pytest.mark.parametrize("name", ui._MONO)
def test_monogram_contrast(name):
    assert ratio(ui.PALETTE[name][0], "#f8f4ec") >= 4.5
