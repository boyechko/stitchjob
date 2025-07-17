import subprocess

def test_stitch_letter_cli_pdf(test_data_session):
    output = subprocess.run(["python3", "stitchjob/stitch_letter.py",
                             test_data_session / "letter.md",
                             "-r", test_data_session / "resume.xml",
                             "-p"])
    assert (test_data_session / "letter.pdf").exists()

def test_stitch_letter_cli_signature_image(test_data_session):
    output = subprocess.run(["python3", "stitchjob/stitch_letter.py",
                             test_data_session / "letter.md",
                            "-r", test_data_session / "resume.xml",
                            "-s", "-S", test_data_session / "signature.png"])
    tex_path = test_data_session / "letter.tex"
    assert tex_path.exists()
    assert "\\includegraphics[height=2em]{signature.png}" in tex_path.read_text()