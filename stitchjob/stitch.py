import argparse
import logging

from stitchjob.stitch_resume import stitch_resume
from stitchjob.stitch_letter import stitch_letter
from stitchjob.shared import *

def main(argv=None):
    try:
        args = parse_args(argv)
        log_level = logging.DEBUG if args.verbose else logging.INFO
        log_setup(log_level)

        if args.command == "resume":
            stitch_resume(args)
        elif args.command == "letter":
            stitch_letter(args)
    except StitchjobException as e:
        log_error_and_exit(e)
    except Exception as e:
        log_error_and_exit(e, "Unhandled error: " + str(e))

def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stitchjob: Tailored resume and letter builder"
    )
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose logging")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Resume subcommand
    resume_parser = subparsers.add_parser("resume", help="Generate LaTeX resume from XML")
    resume_parser.add_argument("input", nargs="?", default="resume/resume.xml",
                               help="Input XML file (default: resume/resume.xml)")
    resume_parser.add_argument("-p", "--pdf", action="store_true",
                               help="Compile the .tex file to PDF using pdflatex")
    resume_parser.add_argument("-P", "--openpdf", action="store_true",
                               help="Compile the .tex file to PDF and open it")

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
    letter_parser.add_argument("-P", "--openpdf", action="store_true",
                               help="Compile the .tex file to PDF and open it")

    return parser.parse_args(argv)

def log_setup(level):
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s',
        stream=sys.stdout,
        force=True)     # <- override prior config (Python 3.8+)

def log_error_and_exit(err: Exception, msg: str | None = None) -> None:
    filename = getattr(err, "filename", None)

    if msg and filename:
        logging.error(msg + f": {filename}")
    elif msg:
        logging.error(msg)
    else:
        logging.error(str(err))

    sys.exit(1)

if __name__ == "__main__":
    main()
