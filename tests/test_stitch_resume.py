import xml.etree.ElementTree as ET

import pytest

from stitchjob.stitch_resume import Resume

def test_valid_resume_from_static_file(test_data_session):
    resume = Resume(test_data_session / "resume.xml")
    assert resume.contact['name'] == "Riley K. Chen"

def test_resume_with_invalid_xml(tmp_path):
    path = tmp_path / "invalid.xml"
    path.write_text("<resume><contact><name>Oops</contact></resume>")
    with pytest.raises(ET.ParseError):
        resume = Resume(path)
