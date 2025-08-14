import argparse
import logging
from pathlib import Path
import re
import subprocess
import sys

def escape_tex(text: str) -> str:
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

def smarten_tex_quotes(text: str) -> str:
    text = re.sub(r'"(.+?)"', r"``\1''", text)
    text = re.sub(r"'(.+?)'", r"`\1'", text)
    return text

def write_tex(tex_path: Path, text: str) -> bool:
    try:
        logging.debug(f"Writing to TeX file '{tex_path}'")
        tex_path.parent.mkdir(parents=True, exist_ok=True)
        tex_path.write_text(text, encoding="utf-8")
        return True
    except PermissionError as e:
        raise CannotWriteToTeXFileError(tex_path, "Permission denied") from e

def maybe_compile_pdf(tex_path: Path) -> Path | None:
    try:
        logging.debug("Compiling PDF file...")
        pdf_path = compile_pdf(tex_path)
    except subprocess.CalledProcessError as e:
        logging.error(e.stdout.decode(errors="replace"))
        logging.error(e.stderr.decode(errors="replace"))
        sys.exit(1)
    else:
        logging.debug(f"PDF file '{pdf_path}' compiled")
        return pdf_path.resolve()

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

def maybe_open_pdf(pdf_path: Path) -> bool | None:
    try:
        logging.debug("Opening PDF file...")
        result = open_pdf(pdf_path)
    except subprocess.CalledProcessError as e:
        logging.error(f"Cannot open the PDF: {str(e)}")
        sys.exit(1)
    else:
        logging.debug(f"Opened PDF file")
        return result

def open_pdf(pdf_path: Path) -> bool:
    result = subprocess.run(
        ["open",
         pdf_path],
         check=True,
         cwd=pdf_path.parent,
         stdout=subprocess.PIPE,
         stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        return False
    return True

# --- Exceptions --- #

class StitchjobException(Exception):
    def __init__(self, message: str, filename: str | Path, reason: str = ""):
        self.message = message
        self.filename = Path(filename) if not isinstance(filename, Path) else filename
        self.reason = reason
        super().__init__(self.__str__())

    def __str__(self):
        if self.reason:
            return f"{self.message}: {self.filename}: {self.reason}"
        else:
            return f"{self.message}: {self.filename}"

class CannotWriteToTeXFileError(StitchjobException):
    def __init__(self, filename: str | Path, reason: str = ""):
        super().__init__("Cannot write to TeX file", filename, reason)

class CannotReadResumeFileError(StitchjobException):
    def __init__(self, filename: str | Path, reason: str = ""):
        super().__init__("Cannot read XML resume file", filename, reason)
