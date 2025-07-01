import xml.etree.ElementTree as ET
import re

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

class Resume:
    def __init__(self, element):
        self.name = XmlHelper.findtext(element, "contact/name")
        self.phone = XmlHelper.findtext(element, "contact/phone")
        self.email = XmlHelper.findtext(element, "contact/email")
        self.location = XmlHelper.findtext(element, "contact/location")
        self.experience_sections = [ExperienceSection(exps_el) for exps_el in element.findall("experiences")]
        self.education_section = EducationSection(element.findall("education")[0])

    def to_latex(self):
        latex = "\\documentclass{rb-resume}\n"
        latex += f"\\setname{{{self.name}}}\n"
        latex += f"\\setemail{{{self.email}}}\n"
        latex += f"\\setphone{{{self.phone}}}\n"
        latex += f"\\setlocation{{{self.location}}}\n"
        latex += "\n\\begin{document}\n\n"
        for exp_sec in self.experience_sections:
            latex += exp_sec.to_latex()
        latex += self.education_section.to_latex()
        latex += "\\end{document}\n"
        return latex

class ExperienceSection:
    def __init__(self, element):
        self.type = element.attrib.get("type")
        self.heading = element.attrib.get("heading", self.type.capitalize() + " Experience")
        self.experiences = [Experience(exp_el) for exp_el in element.findall("experience")]

    def to_latex(self):
        latex = f"\\section*{{{escape_latex(self.heading)}}}\n"
        for exp in self.experiences:
            latex += exp.to_latex() + "\n"
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

class EducationSection:
    def __init__(self, element):
        self.heading = element.attrib.get("heading", "Education")
        self.degrees = [Degree(deg_el) for deg_el in element.findall("degree")]

    def to_latex(self):
        latex = f"\\section*{{{escape_latex(self.heading)}}}\n"
        for deg in self.degrees:
            latex += deg.to_latex()
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

tree = ET.parse("resume.xml")
root = tree.getroot()
resume = Resume(root)

with open("resume.tex", "w") as f:
    f.write(resume.to_latex())
