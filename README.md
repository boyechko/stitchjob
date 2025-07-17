# Stitchjob

**Stitchjob** is a plaintext-first toolchain for assembling custom-fit resumes
from modular parts. Rather than rewriting or cloning past resumes, Stitchjob
encourages thoughtful tailoring by letting you trim, stitch, and combine
prewritten bullet points into job-specific documents.

Built for writers, developers, and anyone tired of one-size-fits-all job applications.

The LaTeX resume class was heavily inspired by [Patrick Benito's resume
template](https://github.com/patrick-benito/pats-resume).

## Requirements

- Python 3.7+
  - frontmatter 3.08+
  - Mako 1.3.10+
- LaTeX installation with `pdflatex`
- Make (optional, for automated builds)

## Description of Use

1. Create a master resume using simple XML (see `resume/example.xml` and
   `resume/template.xml`) that captures your work experience in well-worded
   bullet points describing every significant aspect of what you did.

2. When it comes time to apply for a job, remove irrelevant content, leaving
   only the details that speak directly to what the job posting asks for, saving
   the result as, for example, `resume/resume.xml`.

3. Write a cover letter in Markdown-with-YAML-header-like `letter/letter.md`
   (see `letter/example.md`).

4. If you save the XML resume as `resume/resume.xml` and the letter as
   `letter/letter.md`, you can also just run `make` (or `make all`) to generate
   `resume/resume.tex`, `resume/resume.pdf`, `letter/letter.tex`, and
   `letter/latter.pdf`.

    For arbitrarily named resume file `resume/myresume.xml`, use make targets of
    `resume/myresume.tex` and `resume/myresume.pdf`, depending on what format
    you want. Similarly, for arbitrarily named letter file `letter/myletter.md`,
    you would use make targets of `letter/myletter.tex` and `letter/myletter.pdf`.

    For more control, execute `stitchjob/stitch_resume.py` and `stitchjob/stitch_letter.py` directly.

5. Review the resulting PDFs, make necessary adjustments, and recompile (step
   #4) as needed. Since both the Python script and the generated LaTeX files are
   lightweight, the compilation should be very quick.

## Resume XML Format

Stitchjob resumes are authored in a lightweight XML format that balances
structure with flexibility. The XML file must begin with a `<resume>` root
element and typically includes the following:

- `<contact>`: Your name, email, phone, location, and optional links (e.g., GitHub, LinkedIn).
- `<section>`: Major sections of the resume (e.g., Summary, Key Competencies,
  Experience, Education). Use the `heading` attribute to specify a title;
  optionally, add a `type` for semantic grouping.
- `<skills>`: Inside a section, lists individual `<skill>` elements.
- `<experience>`: Work or project entries, with attributes `begin` and `end`.
  Child elements include `<title>`, `<organization>`, `<location>`, optional
  `<blurb>`, and a list of `<item>` bullet points or freeform text
  `<description>`.
- `<degree>`: For education, including `<date>`, `<type>`, `<field>`, `<school>`, and `<location>`.

The format is intentionally minimal and easy to edit. See
[`resume/example.xml`](resume/example.xml) for a complete, working example. Or
just jump in by copying [`resume/template.xml`](resume/template.xml) and filling
in your details.

*Note:* The content of the XML elements should be plain text that can be passed
directly to LaTeX. Commonly used characters that have special meaning in LaTeX
(i.e. `& % $ # _ ^ ~`) will be escaped, though. Backslashes (`\`) and squiggly
brackets (`{}`) are passed unescaped, allowing for simple LaTeX markup (e.g.
`\\` for newline, `\emph{}` for emphasis, `\textbf{}` for bold, etc.).
Additionally, basic math symbols inside math mode are also handled properly, so
that `$\leftarrow$` will be rendered as `←`, for example.

## Letter Format

Stitchjob letters are written in a text file that uses the familiar Markdown
with YAML header format. However, to keep the dependencies low (i.e. not require
the excellent but heavy [pandoc](https://pandoc.org/)), the file is not actually
parsed as Markdown. Instead, it should be plain text with (optionally) simple
LaTeX formatting (see the note above). Currently recognized YAML header keys are
as follows:

- `recipient`: The name or title of the letter's recipient.
- `company`: The recipient's organization.
- `address`: The organization's address.
- `location`: The city, state, and (if desired) ZIP code of the organization's location.
- `salutation`: The first line of the letter with all necessary punctuation. If
  not supplied, but `recipient` is, defaults to "Dear `recipient`,". If the
  recipient is not specified, defaults to "Dear Hiring Manager,".
- `closing`: The closing line of the letter with all necessary punctuation. If
  not specified, defaults to "Sincerely,".
- `signature`: The signature to appear below the closing line. If more than one
  line is needed, separate the lines with TeX line breaks (double forward
  slashes `\\`; see `letter/example.md`).
- `signature_image`: Path to the image of your signature. It will be rendered to
  fit within two lines of text (`2em` in TeX).

## Directory Structure

```
stitchjob/
├── CHANGELOG.md                # Log of major changes
├── LICENSE                     # Text of the MIT License
├── Makefile                    # Build script for PDF generation
├── pyproject.toml              # Python project specification
├── README.md                   # This file
├── letter/                     # Letter .MD, .TEX, and .PDF files
│   ├── example.md              # Example letter
│   ├── example.tex             # Generated from example.md (auto-generated)
│   ├── example.pdf             # Compiled from example.tex (auto-generated)
│   └── example_signature.png   # Example signature image
├── resume/                     # Resume .XML, .TEX, and .PDF files
│   ├── example.xml             # Full-featured example resume
│   ├── example.tex             # Generated from example.xml
│   ├── example.pdf             # Compiled from example.tex
│   ├── schemas.xml             # XML schemas configuration file
│   ├── template.xml            # Minimal template for starting a new resume
│   └── schema                  # XML schemas
│       ├── resume.dtd          # DTD schema for the resume XML
│       └── resume.rnc          # Relax NG Compact version of DTD schema
├── stitchjob/                  # Python package
│   ├── __init__.py             # Package marker
│   ├── letter.mako             # LaTeX + Mako template for letters
│   ├── shared.py               # Functions and exceptions used by both scripts
│   ├── stitch_resume.py        # Script to convert XML to LaTeX/PDF
│   ├── stitch_letter.py        # Script to convert MD to LaTeX/PDF
│   └── stitched.cls            # LaTeX resume class for Stitchjob resumes
└── tests/                      # Test suite
    ├── test_shared.py
    ├── test_stitch_letter.py
    └── test_stitch_resume.py
```
