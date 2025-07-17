import argparse
from pathlib import Path
import subprocess

import frontmatter
import pytest

from stitchjob.stitch_letter import *

def test_example_letter_parsed_correctly(test_data_session, tmp_path):
    letter = Letter.from_file(test_data_session / "letter.md")
    assert letter.metadata["company"] == "ByteSpring Technologies"
    assert "Documentation Coordinator" in letter.content

def test_letter_without_metadata(tmp_path):
    path = tmp_path / "nometadata.md"
    path.write_text("---\n---\nJust body content.\n")
    letter = Letter.from_file(path)
    assert len(letter.metadata.items()) == 0
    assert "Just body content." in letter.content

def test_signature_image_not_found_exception(test_data_session):
    args = default_args(test_data_session)
    args.signature = True
    args.signature_image = "foobar.png"
    assert not Path("foobar.png").exists()
    with pytest.raises(SignatureImageNotFoundError):
        stitch_letter(args)

def test_stitch_letter_to_tex(test_data_session):
    args = default_args(test_data_session)
    stitch_letter(args)
    assert text_in_tex_file(args, "Documentation Coordinator")

def test_write_tex_raises_exception(test_data):
    args = default_args(test_data)
    tex_path = determine_tex_path(args)
    tex_path.touch(000)
    with pytest.raises(CannotWriteToTeXFileError):
        write_tex(tex_path, "Irrelevant")

def test_stitch_letter_signature_image_from_cli(test_data_session):
    args = default_args(test_data_session)
    args.signature = True
    stitch_letter(args)
    assert text_in_tex_file(args, "\\includegraphics[height=2em]{signature.png}")

def test_stitch_letter_signature_image_from_metadata(test_data):
    letter_path = test_data / "with_signature.md"
    letter_path.write_text("---\nsignature_image: mysig.png\n---\nBody.\n")
    (test_data / "mysig.png").touch()
    args = default_args(test_data)
    args.input = letter_path
    stitch_letter(args)
    assert text_in_tex_file(args, "\\includegraphics[height=2em]{mysig.png}")

# --- Helper Functions --- #

def default_args(dir: Path) -> argparse.Namespace:
    if not dir.is_dir():
        dir = dir.parent
    args = argparse.Namespace(
        input = dir / "letter.md",
        resume = dir / "resume.xml",
        signature = False,
        signature_image = dir / "signature.png",
        output = None,
        pdf = False
    )
    return args

def text_in_tex_file(args: argparse.Namespace, text: str) -> bool:
    tex_path = determine_tex_path(args)
    assert tex_path.exists()
    assert text in tex_path.read_text()
    return True

