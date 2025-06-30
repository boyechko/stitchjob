import xml.etree.ElementTree as ET

class Resume:
    def __init__(self, element):
        self.name = element.findtext("contact/name")
        self.phone = element.findtext("contact/phone")
        self.email = element.findtext("contact/email")
        self.location = element.findtext("contact/location")
        self.experience_sections = [ExperienceSection(exps_el) for exps_el in element.findall("experiences")]

    def to_latex(self):
        latex = "\\documentclass{rb-resume}\n"
        latex += f"\\setname{{{self.name}}}\n"
        latex += f"\\setemail{{{self.email}}}\n"
        latex += f"\\setphone{{{self.phone}}}\n"
        latex += f"\\setlocation{{{self.location}}}\n"
        latex += "\n\\begin{document}\n\n"
        for exp_sec in self.experience_sections:
            latex += exp_sec.to_latex()
        latex += "\\end{document}\n"
        return latex

class ExperienceSection:
    def __init__(self, element):
        self.heading = element.findtext("heading")
        self.experiences = [Experience(exp_el) for exp_el in element.findall("experience")]

    def to_latex(self):
        latex = f"\\section*{{{self.heading}}}\n"
        for exp in self.experiences:
            latex += exp.to_latex() + "\n"
        return latex

class Experience:
    def __init__(self, element):
        self.title = element.findtext("title")
        self.organization = element.findtext("organization")
        self.location = element.findtext("location")
        self.blurb = element.findtext("blurb").strip()
        self.begin = element.attrib.get("begin", "???")
        self.end = element.attrib.get("end", "???")
        self.items = [item.text.strip() for item in element.findall("items/item")]

    def to_latex(self):
        latex = f"\\datedsubsection{{{self.title}}}{{{self.begin} -- {self.end}}}\n"
        latex += f"\\organization{{{self.organization}}}{{{self.location}}}\n"
        if self.blurb:
            latex += f"\\organizationblurb{{{self.blurb}}}\n"
        latex += "\\begin{itemize}\n"
        for item in self.items:
            latex += f"  \\item {item}\n"
        latex += "\\end{itemize}\n"
        return latex

tree = ET.parse("resume.xml")
root = tree.getroot()
resume = Resume(root)

with open("resume.tex", "w") as f:
    f.write(resume.to_latex())
