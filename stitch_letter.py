import argparse
from pathlib import Path
from mako.template import Template
import frontmatter
import stitch_resume

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
    args = parser.parse_args()
    input_path = Path(args.input).resolve()
    resume_path = Path(args.resume)

    # Compute default output path if not provided
    if args.output is None:
        output_path = input_path.with_suffix(".tex")
    else:
        output_path = Path(args.output)

    try:
        resume = stitch_resume.Resume(resume_path)
    except FileNotFoundError as err:
        print(f"Error: XML resume file '{args.resume}' not found")
        exit(1)

    contact = resume.contact
    letter = frontmatter.load(input_path)

    if not args.signature:
        sig_path = None
    elif args.signature and Path(args.signature).exists():
        sig_path = Path(args.signature).resolve()
    else:
        print(f"Error: Signature file '{args.signature}' not found")
        exit(1)

    template = Template(filename='letter/template.mako')

    print(f"Stitching LaTeX file...", end='')
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as file:
            file.write(template.render(contact=contact,
                                    letter=letter,
                                    signature_image=sig_path))
        print("Done")
    except:
        print("Error: Could not stitch together '{output_path}'")
        exit(1)

if __name__ == "__main__":
    main()
