import argparse
from dataclasses import dataclass, field
import logging
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import frontmatter
from frontmatter import Post
from mako.template import Template

from stitchjob.shared import *
from stitchjob.stitch_resume import Contact, Resume

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    try:
        args = parse_args()
        stitch_letter(args)
    except StitchjobException as e:
        log_error_and_exit(e)
    except Exception as e:
        log_error_and_exit(e, "Unhandled error: " + str(e))

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

def stitch_letter(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    resume_path = Path(args.resume)

    logging.debug(f"Parsing Markdown input file '{input_path.name}'")
    letter = Letter.from_file(input_path)

    logging.debug(f"Getting contact information from '{resume_path.name}'")
    letter.contact = get_contact_from_resume(resume_path)

    letter.signature_image = determine_signature_image(args, letter)
    if letter.signature_image:
        logging.debug(f"Using signature image '{letter.signature_image.name}'")

    text = render_tex(letter)
    tex_path = determine_tex_path(args)
    logging.debug(f"Writing LaTeX file '{tex_path}'")
    write_tex(tex_path, text)

    pdf_path = maybe_compile_pdf(args, tex_path)

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

def get_contact_from_resume(resume_path: Path) -> Contact:
    try:
        return Resume(resume_path).contact
    except ET.ParseError as e:
        raise CannotReadResumeFileError(resume_path, "Parse error: " + str(e)) from e
    except FileNotFoundError as e:
        raise CannotReadResumeFileError(resume_path, "File note found") from e
    except PermissionError as e:
        raise CannotReadResumeFileError(resume_path, "Permission denied: " + str(e)) from e

def determine_signature_image(args: argparse.Namespace, letter: Letter) -> Path | None:
    """Return resolved path to signature image or None.

    If `args.signature` is False, return None.

    If signature image is specified in metadata, treat it as relative to the
    input file. Otherwise, use command-line argument (default:
    letter/signature.png), interpreted relative to the script location.

    Raises an error if the resolved file is not found."""
    input_path = Path(args.input)

    if 'signature_image' in letter.metadata:
        # Relative to input file
        sig_image = (input_path.parent / letter.metadata['signature_image']).resolve()
        logging.debug(f"Using signature image '{letter.metadata['signature_image']}' from metadata")
    elif args.signature and args.signature_image:
        # Relative to script
        sig_image = (Path(__file__).parent / args.signature_image).resolve()
        logging.debug(f"Using signature image '{args.signature_image}' from arguments")
    else:
        return None

    if not sig_image.exists():
        # Display path relative to script in the error message
        display_path = sig_image
        try:
            display_path = sig_image.relative_to(Path(__file__).parent)
        except ValueError:
            pass
        raise SignatureImageNotFoundError(display_path)

    # Return image location relative to input file path, if possible
    try:
        return sig_image.relative_to(input_path.parent.resolve())
    except ValueError:
        return sig_image

class SignatureImageNotFoundError(StitchjobException):
    """Signature image is not found despite being specified."""
    def __init__(self, filename: Path):
        super().__init__("Signature image not found", filename)

def render_tex(letter: Letter) -> Path:
    mako_path = Path(__file__).parent / "letter.mako"
    template = Template(filename=str(mako_path))

    letter.content = escape_tex(letter.content)
    for key, val in letter.metadata.items():
        letter.metadata[key] = escape_tex(val)

    return template.render(letter=letter)

def determine_tex_path(args: argparse.Namespace) -> Path:
    if args.output is None:
        return Path(args.input).with_suffix(".tex")
    else:
        return Path(args.output)

def write_tex(tex_path: Path, text: str) -> Path:
    try:
        return _write_tex(tex_path, text)
    except PermissionError as e:
        raise CannotWriteToTeXFileError(tex_path, "Permission denied") from e

def _write_tex(tex_path: Path, text: str) -> Path:
    tex_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tex_path, 'w') as file:
        file.write(text)
    return tex_path

if __name__ == "__main__":
    main()
