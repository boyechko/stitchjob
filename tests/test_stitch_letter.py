import argparse
from pathlib import Path
import subprocess

import frontmatter
import pytest

from stitchjob.stitch_letter import Letter
from stitchjob.stitch_letter import determine_signature_image, SignatureImageNotFound

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

def test_signature_image_not_found(test_data_session, tmp_path):
    args = argparse.Namespace(
        input=test_data_session / "letter.md",
        signature=True,
        signature_image="foobar.png"
    )
    letter = frontmatter.Post(content="")
    assert not Path("foobar.png").exists()
    with pytest.raises(SignatureImageNotFound):
        determine_signature_image(args, letter)

def test_stitch_letter_to_tex(test_data_session):
    output = subprocess.run(["python3", "stitchjob/stitch_letter.py", test_data_session / "letter.md", "-r", test_data_session / "resume.xml"])
    tex_path = test_data_session / "letter.tex"
    assert tex_path.exists()
    assert "Documentation Coordinator" in tex_path.read_text()

def test_stitch_letter_to_pdf(test_data_session):
    output = subprocess.run(["python3", "stitchjob/stitch_letter.py", test_data_session / "letter.md", "-r", test_data_session / "resume.xml", "-p"])
    assert (test_data_session / "letter.pdf").exists()

def test_stitch_letter_signature_image(test_data_session):
    output = subprocess.run(["python3", "stitchjob/stitch_letter.py", test_data_session / "letter.md", "-r", test_data_session / "resume.xml", "-s", "-S", test_data_session / "signature.png"])
    tex_path = test_data_session / "letter.tex"
    assert tex_path.exists()
    assert "\\includegraphics[height=2em]{signature.png}" in tex_path.read_text()
