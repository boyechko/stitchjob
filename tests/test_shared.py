from stitchjob.shared import *

def test_escape_tex_special_characters():
    text = "Improved efficiency by 30%, resulting in $1,000,000 increased profits"
    escaped = escape_tex(text)
    assert r"\%" in escaped
    assert r"\$" in escaped

def test_smarten_tex_quotes():
    text = "some 'single' and \"double\" quotes"
    smartened = smarten_tex_quotes(text)
    assert smartened == "some `single' and ``double'' quotes"
