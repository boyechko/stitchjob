import xml.etree.ElementTree as ET

import pytest

from stitchjob.stitch_resume import *

def test_valid_resume_from_static_file(test_data_session):
    resume = Resume(test_data_session / "resume.xml")
    assert resume.contact['name'] == "Riley K. Chen"

def test_resume_with_invalid_xml(tmp_path):
    path = tmp_path / "invalid.xml"
    path.write_text("<resume><contact><name>Oops</contact></resume>")
    with pytest.raises(CannotParseXMLResumeError):
        resume = Resume(path)

def test_latex_class_is_accessible(test_data):
    ensure_latex_class_accessible(test_data)
    assert (test_data / RESUME_LATEX_CLASS).exists()