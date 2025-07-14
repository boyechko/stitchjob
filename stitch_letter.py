import argparse
from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

import frontmatter
from frontmatter import Post
from mako.template import Template

import stitch_resume
from stitch_resume import Contact
from stitch_resume import LaTeX

def main():
    args = parse_args()

    letter = load_input_file(args)
    letter.contact = load_contact_info(args)
    letter.signature_image = determine_signature_image(args, letter)

    tex_path = try_stitching_tex(args, letter)
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

def load_contact_info(args: argparse.Namespace) -> Contact:
    resume_path = Path(args.resume)
    try:
        print(f"Getting contact information...", end='')
        contact = get_contact_from_resume(resume_path)
        print("Done")
        return contact
    except FileNotFoundError as err:
        print(f"\nError: XML resume file '{resume_path}' not found")
        sys.exit(1)
    except ET.ParseError as err:
        print(f"\nError: Cannot parse '{resume_path}': {err}")
        sys.exit(1)

def get_contact_from_resume(resume_path: Path) -> Contact:
    resume = stitch_resume.Resume(resume_path)
    assert isinstance(resume.contact, Contact)
    return resume.contact

def load_input_file(args: argparse.Namespace) -> Letter:
    input_path = Path(args.input)
    try:
        print(f"Parsing Markdown input file...", end='')
        letter = Letter.from_file(input_path)
        print("Done")
        return letter
    except FileNotFoundError:
        print(f"\nError: Input Markdown file '{input_path}' not found")
        sys.exit(1)
    except Exception as err:
        print(f"\nError: While getting contact info: {err}")
        sys.exit(1)

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
        raise SignatureImageNotFound(sig_image)

    # Return image location relative to input file path, if possible
    try:
        return sig_image.relative_to(input_path.parent.resolve())
    except ValueError:
        return sig_image

class SignatureImageNotFound(Exception):
    """Signature image is not found despite being specified."""
    pass

def try_stitching_tex(args: argparse.Namespace, letter: Letter) -> Path:
    try:
        print(f"Stitching LaTeX file...", end='')
        tex_path = stitch_tex(args, letter)
        print("Done")
        return tex_path
    except PermissionError as err:
        print(f"\nError: Cannot write to '{tex_path}': {err}")

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

def maybe_compile_pdf(args, tex_path: Path) -> Path | None:
    if args.pdf:
        try:
            print("Compiling PDF file...", end='')
            pdf_path = compile_pdf(tex_path)
            print("Done")
            return pdf_path
        except subprocess.CalledProcessError as e:
            print("Error")
            print(e.stdout.decode(errors="replace"))
            print(e.stderr.decode(errors="replace"))
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

if __name__ == "__main__":
    main()
