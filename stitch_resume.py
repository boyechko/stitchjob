import sys
import argparse
import xml.etree.ElementTree as ET
import re
from pathlib import Path

LATEX_ESCAPE = {
    "&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#",
    "_": "\\_", "{": "\\{", "}": "\\}", "~": "\\textasciitilde{}",
    "^": "\\textasciicircum{}", "\\": "\\textbackslash{}",
    "←": "$\\leftarrow$", "→": "$\\rightarrow$", "↔": "$\\leftrightarrow$"
}

def escape_latex(text):
    return "".join(LATEX_ESCAPE.get(c, c) for c in text)

class XmlHelper:
    @staticmethod
    def text(element, default=""):
        text = element.text
        if text:
            return re.sub(r"\s+", " ", text).strip()
        return default

    @staticmethod
    def findtext(element, path, default=""):
        text = element.findtext(path)
        if text:
            return re.sub(r"\s+", " ", text).strip()
        return default

class Section:
    def __str__(self):
        return f"Section({self.type=}, {self.heading=}, {self.children.count()})"

    def __init__(self, element):
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
        #self.children = [Experience(exp_el) for exp_el in element.findall("experience")]

    def to_latex(self):
        latex = f"\\section*{{{escape_latex(self.heading)}}}\n"
        for child in self.children:
            latex += child.to_latex() + "\n"
        return latex

class Experience:
    def __init__(self, element):
        self.title = XmlHelper.findtext(element, "title")
        self.organization = XmlHelper.findtext(element, "organization")
        self.location = XmlHelper.findtext(element, "location")
        self.blurb = XmlHelper.findtext(element, "blurb")
        self.begin = element.attrib.get("begin", "???")
        self.end = element.attrib.get("end", "???")
        self.items = [XmlHelper.text(item) for item in element.findall("items/item")]

    def to_latex(self):
        latex = r"""
        \datedsubsection{%(title)s}{%(begin)s -- %(end)s}
        \organization{%(organization)s}[%(location)s][%(blurb)s]
        """ % {
            'title': escape_latex(self.title),
            'begin': escape_latex(self.begin),
            'end': escape_latex(self.end),
            'organization': escape_latex(self.organization),
            'location': escape_latex(self.location),
            'blurb': escape_latex(self.blurb)
        }
        latex += "\\begin{itemize}\n"
        for item in self.items:
            latex += f"  \\item {escape_latex(item)}\n"
        latex += "\\end{itemize}\n"
        return latex

class Degree:
    def __init__(self, element):
        self.date = XmlHelper.findtext(element, "date")
        self.type = XmlHelper.findtext(element, "type")
        self.field = XmlHelper.findtext(element, "field")
        self.school = XmlHelper.findtext(element, "school")
        self.location = XmlHelper.findtext(element, "location")

    def to_latex(self):
        date = escape_latex(self.date)
        type = escape_latex(self.type)
        field = escape_latex(self.field)
        school = escape_latex(self.school)
        location = escape_latex(self.location)

        return f"\\degree{{{type}}}{{{field}}}{{{school}}}{{{location}}}{{{date}}}\n"

class SkillSection:
    def __init__(self, element):
        self.skills = [Skill(skill_el) for skill_el in element.findall("skill")]

    def to_latex(self):
        latex = f"\\begin{{skills}}\n"
        for skill in self.skills:
            latex += f"\\item {skill.to_latex()}\n"
        latex += "\n\\end{skills}\n"
        return latex

class Skill:
    def __init__(self, element):
        self.name = element.text

    def to_latex(self):
        return escape_latex(self.name)

class Description:
    def __init__(self, element):
        self.text = element.text

    def to_latex(self):
        return escape_latex(self.text)

class Resume:
    """Object representing a resume."""

    def __init__(self, source):
        """Initializes the Resume from source XML file.
        
        Args:
            source (str or file-like): A path to the XML file or an open file-like object.
        """
        self.contact = {}

        root = ET.parse(source).getroot()
        for item in root.findall("./contact")[0]:
            self.contact[item.tag] = item.text
        self.sections = [Section(sec_el) for sec_el in root.findall("section")]

    def to_latex(self):
        latex = "\\documentclass{stitched}\n"

        keys = []
        for key, val in self.contact.items():
            keys.append(f"{key}={{{val}}}")
        latex += "\\setprofile{\n"
        latex += ",\n".join(keys)
        latex += "\n}\n"

        latex += "\n\\begin{document}\n\n"
        for sec in self.sections:
            latex += sec.to_latex()
        latex += "\\end{document}\n"
        return latex

def main():
    parser = argparse.ArgumentParser(description="Generate LaTeX resume from XML")
    parser.add_argument("input", nargs="?",
                        default="resume/resume.xml",
                        help="Input XML file (default: resume/resume.xml)")
    parser.add_argument("-o", "--output", type=str,
                        help="Output LaTeX file (default: <input>.tex)")
    args = parser.parse_args()
    input_path = Path(args.input).resolve()

    # Compute default output path if not provided
    if args.output is None:
        output_path = input_path.with_suffix(".tex")
    else:
        output_path = Path(args.output)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        resume = Resume(input_path)
    except FileNotFoundError as err:
        print(f"Error: File '{args.input}' not found.")

    with output_path.open("w") as f:
        latex = resume.to_latex()
        print(latex, file=f)

if __name__ == "__main__":
    main()
