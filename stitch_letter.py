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

def main():
    parser = argparse.ArgumentParser(description="Generate LaTeX cover letter from Markdown")
    parser.add_argument("input", nargs="?",
                        default="letter/letter.md",
                        help="Input Markdown file (default: letter/letter.md)")
    parser.add_argument("-r", "--resume", type=str,
                        default="resume/resume.xml",
                        help="XML resume file with contact info (default: resume/resume.xml)")
    parser.add_argument("-s", "--signature", type=str,
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

    if not args.signature:
        sig_path = None
    elif args.signature and Path(args.signature).exists():
        sig_path = Path(args.signature).resolve()
        try:
            sig_path = sig_path.relative_to(input_path.parent)
        except ValueError:
            pass
    else:
        print(f"Error: Signature file '{args.signature}' not found")
        sys.exit(1)

    try:
        template = Template(filename='letter/template.mako')
    except Exception as err:
        print(f"Error: {err}")
        sys.exit(1)

    print(f"Stitching LaTeX file...", end='')
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
