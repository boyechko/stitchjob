import argparse
from importlib.resources import files
import logging
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

from stitchjob.shared import *

RESUME_LATEX_CLASS = files("stitchjob") / "stitched.cls"

def stitch_resume(args: argparse.Namespace):
    input_path = Path(args.input).resolve()
    logging.debug(f"Parsing resume XML file '{input_path}'")
    resume = Resume(input_path)

    output_path = input_path.with_suffix(".tex")
    logging.debug(f"Stitching LaTeX file '{output_path}'")
    write_tex(output_path, latex_metadata() + resume.to_latex())

    logging.debug(f"Ensuring '{RESUME_LATEX_CLASS.name}' is available")
    ensure_latex_class_available(output_path)

    pdf_path = None
    if args.pdf or args.openpdf:
        pdf_path = maybe_compile_pdf(output_path)

    if args.openpdf and pdf_path:
        maybe_open_pdf(pdf_path)
    elif args.openpdf:
        logging.error("PDF file not generated, cannot open")

def ensure_latex_class_available(tex_path: Path):
    """Ensure that 'stitched.cls' is available in TeX file's directory."""
    cls_src = files("stitchjob") / "stitched.cls"
    cls_dst = tex_path.parent / "stitched.cls"
    try:
        shutil.copy(cls_src, cls_dst)
    except shutil.SameFileError:
        # If there is already a symlink to stitched.cls in tex_path, don't need
        # to copy the file.
        pass

class Resume:
    def __init__(self, xml_file: Path):
        try:
            root = ET.parse(xml_file).getroot()
            self.contact = Contact(root)
            self.sections = [Section.create(sec_el) for sec_el in root.findall("section")]
        except ET.ParseError as e:
            raise CannotParseXMLResumeError(xml_file, str(e)) from e
        except FileNotFoundError as e:
            raise CannotReadResumeFileError(xml_file, "File not found") from e
        except PermissionError as e:
            raise CannotReadResumeFileError(xml_file, "Permission denied") from e

    def to_latex(self) -> str:
        output = "\\documentclass{stitched}\n"

        output += self.contact.to_latex()

        output += "\n\\begin{document}\n\n"
        for sec in self.sections:
            output += sec.to_latex()
        output += "\\end{document}\n"
        return output

class CannotParseXMLResumeError(StitchjobException):
    def __init__(self, filename: Path, reason: str = ""):
        super().__init__("Cannot parse XML resume", filename, reason)

class Contact:
    def __init__(self, source: Path | ET.Element):
        if not isinstance(source, ET.Element):
            source = ET.parse(source).getroot()

        self.values = {}
        contact = source.findall("./contact")[0]
        for item in contact:
            self.values[item.tag] = item.text
        if 'website' in self.values:
            self.values['website'] = re.sub(r'https*://', "", self.values['website'])

    def __getitem__(self, key: str):
        return self.values[key]

    def items(self):
        return self.values.items()

    def to_latex(self) -> str:
        keys = []
        output = "\\setprofile{\n"
        for key, val in self.values.items():
            keys.append(f"{key}={{{val}}}")
        output += ",\n".join(keys)
        output += "\n}\n"
        return output

class Section:
    @classmethod
    def create(cls, element: ET.Element):
        section_type = element.attrib.get("type")
        if section_type == "education":
            return EducationSection(element)
        return cls(element)

    def __str__(self):
        return f"Section({self.type=}, {self.heading=}, {len(self.children)})"

    def __init__(self, element: ET.Element):
        self.type = element.attrib.get("type")
        self.heading = element.attrib.get("heading", "Section")
        self.children = []
        for child in element:
            obj = None
            if child.tag == "experience":
                obj = Experience(child)
            elif child.tag == "degree":
                obj = Degree(child)
            elif child.tag == "skills":
                obj = SkillSection(child)
            elif child.tag == "description":
                obj = Description(child)
            else:
                raise Exception(f"Don't know how to handle `{child.tag}' child")
            self.children.append(obj)

    def to_latex(self) -> str:
        output = f"\\section{{{escape_tex(self.heading)}}}\n"
        for child in self.children:
            output += child.to_latex() + "\n"
        return output

class EducationSection(Section):
    def to_latex(self) -> str:
        output = f"\\section{{{escape_tex(self.heading)}}}\n"
        output += "\\begin{education}\n"
        for child in self.children:
            output += child.to_latex() + "\n"
        output += "\\end{education}\n"
        return output

class Experience:
    def __init__(self, element: ET.Element):
        self.title = XmlHelper.findtext(element, "title")
        self.organization = XmlHelper.findtext(element, "organization")
        self.location = XmlHelper.findtext(element, "location")
        self.blurb = XmlHelper.findtext(element, "blurb")
        self.begin = element.attrib.get("begin", "???")
        self.end = element.attrib.get("end", "???")
        self.items = [XmlHelper.text(item) for item in element.findall("items/item")]

    def to_latex(self) -> str:
        output = r"""
        \experience{%(begin)s -- %(end)s}{%(title)s}{%(organization)s}[%(location)s]
        """ % {
            'title': escape_tex(self.title),
            'begin': escape_tex(self.begin),
            'end': escape_tex(self.end),
            'organization': escape_tex(self.organization),
            'location': escape_tex(self.location)
        }
        if self.blurb:
            output += f"\\blurb{{{smarten_tex_quotes(escape_tex(self.blurb))}}}\n"
        output += "\\begin{duties}\n"
        for item in self.items:
            output += f"  \\item {smarten_tex_quotes(escape_tex(item))}\n"
        output += "\\end{duties}\n"
        return output

class Degree:
    def __init__(self, element: ET.Element):
        self.date = XmlHelper.findtext(element, "date")
        self.type = XmlHelper.findtext(element, "type")
        self.field = XmlHelper.findtext(element, "field")
        self.school = XmlHelper.findtext(element, "school")
        self.location = XmlHelper.findtext(element, "location")

    def to_latex(self) -> str:
        date = escape_tex(self.date)
        type = escape_tex(self.type)
        field = escape_tex(self.field)
        school = escape_tex(self.school)
        location = escape_tex(self.location)

        return f"\\degree{{{type}}}{{{field}}}{{{school}}}{{{location}}}{{{date}}}\n"

class SkillSection:
    def __init__(self, element: ET.Element):
        self.skills = [Skill(skill_el) for skill_el in element.findall("skill")]

    def to_latex(self) -> str:
        output = f"\\begin{{skills}}\n"
        for skill in self.skills:
            output += f"\\item {skill.to_latex()}\n"
        output += "\n\\end{skills}\n"
        return output

class Skill:
    def __init__(self, element: ET.Element):
        self.name = element.text

    def to_latex(self) -> str:
        return smarten_tex_quotes(escape_tex(self.name))

class Description:
    def __init__(self, element: ET.Element):
        self.text = element.text

    def to_latex(self) -> str:
        return smarten_tex_quotes(escape_tex(self.text))

class XmlHelper:
    @staticmethod
    def text(element: ET.Element, default: str = "") -> str:
        text = element.text
        if text:
            return re.sub(r"\s+", " ", text).strip()
        return default

    @staticmethod
    def findtext(element: ET.Element, path: str, default: str = "") -> str:
        text = element.findtext(path)
        if text:
            return re.sub(r"\s+", " ", text).strip()
        return default
