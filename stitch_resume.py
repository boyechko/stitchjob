import argparse
import logging
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    try:
        args = parse_args()

        logging.debug("Parsing resume XML file...")
        input_path = Path(args.input).resolve()
        resume = Resume(input_path)

        logging.debug("Stitching LaTeX file...")
        output_path = determine_output_path(args)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(resume.to_latex() + "\n", encoding="utf-8")

        maybe_compile_pdf(args, output_path)

    except FileNotFoundError:
        logging.error(f"File '{args.input}' not found")
        sys.exit(1)
    except ET.ParseError as err:
        logging.error(f"Failed to parse '{input_path}': {err}")
        sys.exit(1)
    except PermissionError as err:
        logging.error(f"Cannot write to '{output_path}': {err}")
        sys.exit(1)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate LaTeX resume from XML")
    parser.add_argument("input", nargs="?",
                        default="resume/resume.xml",
                        help="Input XML file (default: resume/resume.xml)")
    parser.add_argument("-o", "--output", type=str,
                        help="Output LaTeX file (default: <input>.tex)")
    parser.add_argument("-p", "--pdf", action="store_true",
                        help="Compile the .tex file to PDF using pdflatex")
    return parser.parse_args()

def determine_output_path(args: argparse.Namespace) -> Path:
    """Compute default output path if not provided."""
    if args.output is None:
        return Path(args.input).with_suffix(".tex")
    else:
        return Path(args.output)

def maybe_compile_pdf(args: argparse.Namespace, tex_path: Path) -> Path | None:
    if args.pdf:
        try:
            logging.debug("Compiling PDF file...")
            pdf_path = compile_pdf(tex_path)
            return pdf_path
        except subprocess.CalledProcessError as e:
            logging.error(e.stdout.decode(errors="replace"))
            logging.error(e.stderr.decode(errors="replace"))
            sys.exit(1)

def compile_pdf(tex_path: Path) -> Path:
    resolved_tex_path = tex_path.resolve()
    result = subprocess.run(
        ["pdflatex",
         "-interaction=nonstopmode",
         f"-output-directory={resolved_tex_path.parent}",
         resolved_tex_path.name],
        check=True,
        cwd=resolved_tex_path.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return tex_path.with_suffix(".pdf")

class Resume:
    def __init__(self, xml_file: Path):
        root = ET.parse(xml_file).getroot()
        self.contact = Contact(root)
        self.sections = [Section(sec_el) for sec_el in root.findall("section")]

    def to_latex(self) -> str:
        latex = "\\documentclass{stitched}\n"

        latex += self.contact.to_latex()

        latex += "\n\\begin{document}\n\n"
        for sec in self.sections:
            latex += sec.to_latex()
        latex += "\\end{document}\n"
        return latex

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
        latex = "\\setprofile{\n"
        for key, val in self.values.items():
            keys.append(f"{key}={{{val}}}")
        latex += ",\n".join(keys)
        latex += "\n}\n"
        return latex

class Section:
    def __str__(self):
        return f"Section({self.type=}, {self.heading=}, {self.children.count()})"

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
        #self.children = [Experience(exp_el) for exp_el in element.findall("experience")]

    def to_latex(self) -> str:
        latex = f"\\section*{{{LaTeX.escape(self.heading)}}}\n"
        for child in self.children:
            latex += child.to_latex() + "\n"
        return latex

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
        latex = r"""
        \datedsubsection{%(title)s}{%(begin)s -- %(end)s}
        \organization{%(organization)s}[%(location)s][%(blurb)s]
        """ % {
            'title': LaTeX.escape(self.title),
            'begin': LaTeX.escape(self.begin),
            'end': LaTeX.escape(self.end),
            'organization': LaTeX.escape(self.organization),
            'location': LaTeX.escape(self.location),
            'blurb': LaTeX.smarten_quotes(LaTeX.escape(self.blurb))
        }
        latex += "\\begin{itemize}\n"
        for item in self.items:
            latex += f"  \\item {LaTeX.escape(item)}\n"
        latex += "\\end{itemize}\n"
        return latex

class Degree:
    def __init__(self, element: ET.Element):
        self.date = XmlHelper.findtext(element, "date")
        self.type = XmlHelper.findtext(element, "type")
        self.field = XmlHelper.findtext(element, "field")
        self.school = XmlHelper.findtext(element, "school")
        self.location = XmlHelper.findtext(element, "location")

    def to_latex(self) -> str:
        date = LaTeX.escape(self.date)
        type = LaTeX.escape(self.type)
        field = LaTeX.escape(self.field)
        school = LaTeX.escape(self.school)
        location = LaTeX.escape(self.location)

        return f"\\degree{{{type}}}{{{field}}}{{{school}}}{{{location}}}{{{date}}}\n"

class SkillSection:
    def __init__(self, element: ET.Element):
        self.skills = [Skill(skill_el) for skill_el in element.findall("skill")]

    def to_latex(self) -> str:
        latex = f"\\begin{{skills}}\n"
        for skill in self.skills:
            latex += f"\\item {skill.to_latex()}\n"
        latex += "\n\\end{skills}\n"
        return latex

class Skill:
    def __init__(self, element: ET.Element):
        self.name = element.text

    def to_latex(self) -> str:
        return LaTeX.smarten_quotes(LaTeX.escape(self.name))

class Description:
    def __init__(self, element: ET.Element):
        self.text = element.text

    def to_latex(self) -> str:
        return LaTeX.smarten_quotes(LaTeX.escape(self.text))

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

class LaTeX:
    @staticmethod
    def smarten_quotes(text: str) -> str:
        text = re.sub(r'"(.+?)"', r"``\1''", text)
        text = re.sub(r"'(.+?)'", r"`\1'", text)
        return text

    @staticmethod
    def escape(text: str) -> str:
        special = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',  # this will be skipped inside math
            '#': r'\#',
            '_': r'\_',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
        }

        # Pattern to match inline math like $...$
        math_pattern = re.compile(r'\$(.+?)\$')

        # Split text into segments: math and non-math
        parts = []
        last_end = 0

        for match in math_pattern.finditer(text):
            # Text before math → escape
            before = text[last_end:match.start()]
            for char, replacement in special.items():
                if char == '$':
                    continue  # don't escape $ outside math yet
                before = before.replace(char, replacement)
            before = before.replace('$', r'\$')  # escape remaining dollar signs outside math

            # Math content → leave as-is
            math = match.group(0)  # includes surrounding $...$

            parts.append(before)
            parts.append(math)
            last_end = match.end()

        # Handle the tail (after last match)
        after = text[last_end:]
        for char, replacement in special.items():
            if char == '$':
                continue
            after = after.replace(char, replacement)
        after = after.replace('$', r'\$')

        parts.append(after)

        return ''.join(parts)

if __name__ == "__main__":
    main()
