import subprocess
import sys
import argparse
from pathlib import Path
from mako.template import Template
import frontmatter
import xml.etree.ElementTree as ET
import stitch_resume

def compile_pdf(tex_path: Path):
    """Compile the given LaTeX file into a PDF using pdflatex."""
    tex_path = tex_path.resolve()

    print("Compiling PDF file...", end='')
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", f"-output-directory={tex_path.parent}", tex_path.name],
            check=True,
            cwd=tex_path.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Done")
    except subprocess.CalledProcessError as e:
        print("\nError: ")
        print(e.stdout.decode(errors="replace"))
        print(e.stderr.decode(errors="replace"))
        sys.exit(1)

def signature_image(args: argparse.Namespace, metadata: dict[str, str]) -> Path | None:
    """Return resolved path to signature image or None.

    If `args.signature` is False, return None.

    If signature image is specified in metadata, treat it as relative to the
    input file. Otherwise, use command-line argument (default:
    letter/signature.png), interpreted relative to the script location.

    Raises an error if the resolved file is not found."""
    input_path = Path(args.input)

    if not args.signature:
        return None
    if 'signature_image' in metadata:
        # Relative to input file
        sig_path = (input_path.parent / metadata['signature_image']).resolve()
    else:
        # Relative to script
        sig_path = (Path(__file__).parent / args.signature_image).resolve()

    if not sig_path.exists():
        # Display path relative to script in the error message
        display_path = sig_path
        try:
            display_path = sig_path.relative_to(Path(__file__).parent)
        except ValueError:
            pass
        print(f"\nError: Signature file '{display_path}' not found")
        sys.exit(1)

    # Return image location relative to input file path
    try:
        return sig_path.relative_to(input_path.parent.resolve())
    except ValueError:
        return sig_path

def main():
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
    args = parser.parse_args()
    input_path = Path(args.input).resolve()
    resume_path = Path(args.resume)

    # Compute default output path if not provided
    if args.output is None:
        output_path = input_path.with_suffix(".tex")
    else:
        output_path = Path(args.output)

    print(f"Getting contact information...", end='')
    try:
        resume = stitch_resume.Resume(resume_path)
        contact = resume.contact
        print("Done")
    except FileNotFoundError as err:
        print(f"\nError: XML resume file '{args.resume}' not found")
        sys.exit(1)
    except ET.ParseError as err:
        print(f"\nError: Cannot parse '{resume_path}': {err}")
        sys.exit(1)

    print(f"Parsing Markdown input file...", end='')
    try:
        parsed = frontmatter.load(input_path)
        letter = {}; letter['body'] = stitch_resume.LaTeX.escape(parsed.content)
        for key, val in parsed.metadata.items():
            letter[key] = stitch_resume.LaTeX.escape(val)
        print("Done")
    except FileNotFoundError:
        print(f"Error: Input Markdown file '{input_path}' not found")
        sys.exit(1)
    except Exception as err:
        print(f"\nError: {err}")
        sys.exit(1)

    try:
        template = Template(filename='letter/template.mako')
    except Exception as err:
        print(f"Error: {err}")
        sys.exit(1)

    print(f"Stitching LaTeX file...", end='')
    sig_path = signature_image(args, parsed.metadata)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as file:
            file.write(template.render(contact=contact,
                                       letter=letter,
                                       signature_image=sig_path))
        print("Done")
    except PermissionError as err:
        print(f"\nError: Cannot write to '{output_path}': {err}")
    except Exception as err:
        print(f"\nError: {err}")
        sys.exit(1)

    if args.pdf:
        compile_pdf(output_path)

if __name__ == "__main__":
    main()
