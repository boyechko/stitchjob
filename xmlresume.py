import xml.etree.ElementTree as ET

def format_experience_section(heading, experiences):
    latex = r"\section*{%(heading)s}" % {'heading': heading}
    latex += "\n"
    for exp in experiences:
        datedsubsection = r"\datedsubsection{%(title)s}{%(begin)s -- %(end)s}"
        latex += datedsubsection % {'title': exp['title'],
                                    'begin': exp['begin'],
                                    'end': exp['end']}
        organization = r"\organization{%(organization)s}{%(location)s}"
        latex += "\n" + organization % {'organization': exp['organization'],
                                        'location': exp['location']}
        if exp.get("blurb"):
            latex += f"\n\\organizationblurb{{{exp['blurb']}}}\n"
        latex += "\n\\begin{itemize}\n"
        for item in exp['items']:
            latex += f"  \\item {item}\n"
        latex += "\\end{itemize}\n\n"
    return latex

def experience_sections():
    latex = ''
    exp_containers = root.findall("experiences")
    for container in exp_containers:
        heading = container.findtext("heading")
        exps = []
        for exp_sec in container.findall("experience"):
            exp = {
                "title": exp_sec.findtext("title"),
                "organization": exp_sec.findtext("organization"),
                "location": exp_sec.findtext("location"),
                "blurb": exp_sec.findtext("blurb").strip(),
                "begin": exp_sec.attrib.get("begin", "???"),
                "end": exp_sec.attrib.get("end", "???"),
                "items": [item.text.strip() for item in exp_sec.findall(".//item")],
            }
            exps.append(exp)
        latex += format_experience_section(heading, exps)
    return latex

def build_resume():
    latex = "\\documentclass{rb-resume}\n"
    latex += r'''
    \setname{%(name)s}
    \setemail{%(email)s}
    \setphone{%(phone)s}
    \setlocation{%(location)s}
    ''' % {
        "name": root.findtext("contact/name"),
        "email": root.findtext("contact/email"),
        "phone": root.findtext("contact/phone"),
        "location": root.findtext("contact/location"),
    }
    latex += "\n\\begin{document}\n\n"
    latex += experience_sections()
    latex += "\\end{document}\n"
    return latex

tree = ET.parse("resume.xml")
root = tree.getroot()

with open("resume.tex", "w") as f:
    f.write(build_resume())
