import argparse

from stitchjob.stitch_resume import stitch_resume
from stitchjob.stitch_letter import stitch_letter

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Stitchjob: Tailored resume and letter builder"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Resume subcommand
    resume_parser = subparsers.add_parser("resume", help="Generate LaTeX resume from XML")
    resume_parser.add_argument("input", nargs="?", default="resume/resume.xml",
                               help="Input XML file (default: resume/resume.xml)")
    resume_parser.add_argument("-p", "--pdf", action="store_true",
                               help="Compile the .tex file to PDF using pdflatex")

    # Letter subcommand
    letter_parser = subparsers.add_parser("letter",
                                          help="Generate LaTeX cover letter from Markdown")
    letter_parser.add_argument("input", nargs="?", default="letter/letter.md",
                               help="Input Markdown file (default: letter/letter.md)")
    letter_parser.add_argument("-r", "--resume", type=str, default="resume/resume.xml",
                               help="XML resume file with contact info \
                               (default: resume/resume.xml)")
    letter_parser.add_argument("-s", "--signature", action="store_true",
                               help="Include graphic signature")
    letter_parser.add_argument("-S", "--signature_image", type=str,
                               default="letter/signature.png",
                               help="Image of the signature to use \
                               (default: letter/signature.png)")
    letter_parser.add_argument("-o", "--output", type=str,
                               help="Output LaTeX file (default: <input>.tex)")
    letter_parser.add_argument("-p", "--pdf", action="store_true",
                               help="Compile the .tex file to PDF using pdflatex")

    args = parser.parse_args(argv)

    # Placeholder dispatch
    if args.command == "resume":
        stitch_resume(args)
    elif args.command == "letter":
        stitch_letter(args)

if __name__ == "__main__":
    main()
