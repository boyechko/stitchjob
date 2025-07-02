import sys
import argparse
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
        self.linkedin = XmlHelper.findtext(element, "contact/linkedin")
        self.github = XmlHelper.findtext(element, "contact/github")
        self.experience_sections = [ExperienceSection(exps_el) for exps_el in element.findall("experiences")]
        self.education_section = EducationSection(element.findall("education")[0])
        self.skill_section = SkillSection(element.findall("skills")[0])

    def to_latex(self):
        latex = "\\documentclass{patchworker}\n"
        latex += f"""
\\setprofile{{
name={{{escape_latex(self.name)}}},
email={{{escape_latex(self.email)}}},
phone={{{escape_latex(self.phone)}}},
location={{{escape_latex(self.location)}}},
linkedin={{{escape_latex(self.linkedin)}}},
github={{{escape_latex(self.github)}}}
}}
"""
        latex += "\n\\begin{document}\n\n"
        latex += self.skill_section.to_latex()
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

class SkillSection:
    def __init__(self, element):
        self.heading = element.attrib.get("heading", "Skills")
        self.skills = [Skill(skill_el) for skill_el in element.findall("skill")]

    def to_latex(self):
        latex = f"\\begin{{skills}}{{{escape_latex(self.heading)}}}\n"
        for skill in self.skills:
            latex += f"\\item {skill.to_latex()}\n"
        latex += "\n\\end{skills}\n"
        return latex

class Skill:
    def __init__(self, element):
        self.name = element.text

    def to_latex(self):
        return escape_latex(self.name)

def main():
    parser = argparse.ArgumentParser(description="Generate LaTeX resume from XML")
    parser.add_argument("input", nargs="?", default="resume.xml", help="Input XML file (default: resume.xml)")
    parser.add_argument("-o", "--output",
                        type=argparse.FileType("w"), 
                        default=sys.stdout,
                        help="Output LaTeX file (default: stdout)")
    args = parser.parse_args()

    tree = ET.parse(args.input)
    root = tree.getroot()
    resume = Resume(root)
    latex = resume.to_latex()

    print(latex, file=args.output)

if __name__ == "__main__":
    main()
