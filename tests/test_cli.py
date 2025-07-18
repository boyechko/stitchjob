from pathlib import Path
import subprocess

import pytest

# --- Letter --- #

@pytest.mark.slow
def test_stitch_letter_cli_pdf(test_data_session):
    output = subprocess.run(["stitch", "letter",
                             test_data_session / "letter.md",
                             "-r", test_data_session / "resume.xml",
                             "-p"])
    assert (test_data_session / "letter.pdf").exists()

def test_stitch_letter_cli_signature_image(test_data_session):
    output = subprocess.run(["stitch", "letter",
                             test_data_session / "letter.md",
                            "-r", test_data_session / "resume.xml",
                            "-s", "-S", test_data_session / "signature.png"])
    tex_path = test_data_session / "letter.tex"
    assert tex_path.exists()
    assert "\\includegraphics[height=2em]{signature.png}" in tex_path.read_text()

# --- Resume --- #

def test_stitch_resume_cli_to_tex(test_data):
    output = subprocess.run(["stitch", "resume", test_data / "resume.xml"])
    tex_path = test_data / "resume.tex"
    assert tex_path.exists()
    assert r"\organization{UC Berkeley Library}" in tex_path.read_text()

@pytest.mark.slow
def test_stitch_resume_cli_pdf(test_data):
    output = subprocess.run(["stitch", "resume", test_data / "resume.xml", "-p"])
    assert (test_data / "resume.pdf").exists()
