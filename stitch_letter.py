import argparse
from dataclasses import dataclass, field
import logging
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

import frontmatter
from frontmatter import Post
from mako.template import Template

from latex import LaTeX
from stitch_resume import Contact, Resume, maybe_compile_pdf, compile_pdf

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    try:
        args = parse_args()
        input_path = Path(args.input)
        resume_path = Path(args.resume)

        logging.debug(f"Parsing Markdown input file '{input_path.name}'")
        letter = Letter.from_file(input_path)

        logging.debug(f"Getting contact information from '{resume_path.name}'")
        letter.contact = Resume(resume_path).contact

        letter.signature_image = determine_signature_image(args, letter)
        if letter.signature_image:
            logging.debug(f"Using signature image '{letter.signature_image.name}'")

        logging.debug("Stitching LaTeX file")
        tex_path = stitch_tex(args, letter)
        logging.debug(f"LaTeX file '{tex_path}' stitched")

        pdf_path = maybe_compile_pdf(args, tex_path)
    except FileNotFoundError as err:
        log_error_and_exit(err, "File not found")
    except PermissionError as err:
        log_error_and_exit(err, f"Permission denied when writing '{tex_path}'")
    except ET.ParseError as err:
        log_error_and_exit(err, f"Cannot parse '{resume_path}'")
    except SignatureImageNotFound as err:
        log_error_and_exit(err)

def log_error_and_exit(err: Exception, msg: str | None = None) -> None:
    filename = getattr(err, "filename", None)

    if msg and filename:
        logging.error(msg + f": {filename}")
    elif msg:
        logging.error(msg)
    else:
        logging.error(str(err))

    sys.exit(1)

@dataclass
class Letter:
    contact: Contact | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    content: str | None = None
    signature_image: Path | None = None

    @classmethod
    def from_file(cls, path: Path) -> "Letter":
        post = frontmatter.loads(path.read_text())
        return cls(metadata=post.metadata, content=post.content)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate LaTeX cover letter from Markdown")
    parser.add_argument("input", nargs="?",
                        default="letter/letter.md",
                        help="Input Markdown file (default: letter/letter.md)")
    parser.add_argument("-r", "--resume", type=str,
                        default="resume/resume.xml",
                        help="XML resume file with contact info (default: resume/resume.xml)")
    parser.add_argument("-s", "--signature", action="store_true",
                        help="Include graphic signature")
    parser.add_argument("-S", "--signature_image", type=str,
                        default="letter/signature.png",
                        help="Image of the signature to use (default: letter/signature.png)")
    parser.add_argument("-o", "--output", type=str,
                        help="Output LaTeX file (default: <input>.tex)")
    parser.add_argument("-p", "--pdf", action="store_true",
                        help="Compile the .tex file to PDF using pdflatex")
    return parser.parse_args()

def determine_signature_image(args: argparse.Namespace, letter: Letter) -> Path | None:
    """Return resolved path to signature image or None.

    If `args.signature` is False, return None.

    If signature image is specified in metadata, treat it as relative to the
    input file. Otherwise, use command-line argument (default:
    letter/signature.png), interpreted relative to the script location.

    Raises an error if the resolved file is not found."""
    input_path = Path(args.input)

    if not args.signature:
        return None
    if 'signature_image' in letter.metadata:
        # Relative to input file
        sig_image = (input_path.parent / letter.metadata['signature_image']).resolve()
    else:
        # Relative to script
        sig_image = (Path(__file__).parent / args.signature_image).resolve()

    if not sig_image.exists():
        # Display path relative to script in the error message
        display_path = sig_image
        try:
            display_path = sig_image.relative_to(Path(__file__).parent)
        except ValueError:
            pass
        raise SignatureImageNotFound(display_path)

    # Return image location relative to input file path, if possible
    try:
        return sig_image.relative_to(input_path.parent.resolve())
    except ValueError:
        return sig_image

class SignatureImageNotFound(Exception):
    """Signature image is not found despite being specified."""
    def __init__(self, path: Path):
        self.path = path
        super().__init__(f"Signature image not found: {path}")

def stitch_tex(args: argparse.Namespace, letter: Letter) -> Path:
    tex_path = determine_tex_path(args)
    template = Template(filename='letter/template.mako')

    letter.content = LaTeX.escape(letter.content)
    for key, val in letter.metadata.items():
        letter.metadata[key] = LaTeX.escape(val)

    tex_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tex_path, 'w') as file:
        file.write(template.render(letter=letter))
    return tex_path

def determine_tex_path(args: argparse.Namespace) -> Path:
    if args.output is None:
        return Path(args.input).with_suffix(".tex")
    else:
        return Path(args.output)

if __name__ == "__main__":
    main()
