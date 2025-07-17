from pathlib import Path

from stitchjob.stitch import *

def test_stitch_letter_generates_tex(test_data):
    letter_path = test_data / "letter.md"
    resume_path = test_data / "resume.xml"
    signature_path = test_data / "signature.png"
    main(["letter", str(letter_path), "--resume", str(resume_path),
          "--signature", "--signature_image", str(signature_path),
          "--pdf"])
    expected_tex = letter_path.with_suffix(".tex")
    assert expected_tex.exists()
    assert r"\documentclass[12pt]{article}" in expected_tex.read_text()

def test_stitch_resume_generates_tex(test_data):
    input_path = test_data / "resume.xml"
    main(["resume", str(input_path)])
    expected_tex = input_path.with_suffix(".tex")
    assert expected_tex.exists()
    assert expected_tex.read_text().startswith(r"\documentclass")

def test_stitch_resume_compiles_pdf(test_data, capsys):
    input_path = test_data / "resume.xml"
    main(["resume", str(input_path), "--pdf"])
    out, _ = capsys.readouterr()
    expected_pdf = input_path.with_suffix(".pdf")
    assert expected_pdf.exists()

def test_stitch_resume_prints_debug_messages(test_data, capsys):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    main(["resume", str(test_data / "resume.xml")])
    out, _ = capsys.readouterr()
    assert "DEBUG:" in out
