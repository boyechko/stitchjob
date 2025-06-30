import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader

tree = ET.parse("resume.xml")
root = tree.getroot()

contact = {
    "name": root.findtext("contact/name"),
    "email": root.findtext("contact/email"),
    "phone": root.findtext("contact/phone"),
    "location": root.findtext("contact/location"),
}

jobs_heading = root.findtext(".//experiences[@type='professional']/heading")
jobs = []
for exp in root.findall(".//experiences[@type='professional']/experience"):
    job = {
        "title": exp.findtext("title"),
        "organization": exp.findtext("organization"),
        "location": exp.findtext("location"),
        "blurb": exp.findtext("blurb"),
        "begin": exp.findtext("dates/begin"),
        "end": exp.findtext("dates/end"),
        "bullets": [item.text.strip() for item in exp.findall(".//item")],
    }
    jobs.append(job)

env = Environment(
    loader=FileSystemLoader('.'),
    block_start_string='\\BLOCK{',
    block_end_string='}',
    variable_start_string='\\VAR{',
    variable_end_string='}',
    comment_start_string='\\#{',
    comment_end_string='}',
    trim_blocks=True,
    autoescape=False
)
template = env.get_template('template.tex')

latex = template.render(
    name=contact["name"],
    email=contact["email"],
    phone=contact["phone"],
    location=contact["location"],
    jobs_heading=jobs_heading,
    jobs=jobs
)

with open("resume.tex", "w") as f:
    f.write(latex)

