# Stitchjob

**Stitchjob** is a plaintext-first toolchain for assembling custom-fit resumes
from modular parts. Rather than rewriting or cloning past resumes, Stitchjob
encourages thoughtful tailoring by letting you trim, stitch, and combine
prewritten bullet points into job-specific documents.

Built for writers, developers, and anyone tired of one-size-fits-all job applications.

## Requirements

- Python 3.7+
- LaTeX installation with `pdflatex`
- Make (optional, for automated builds)

## Description of Use

1. Create a master resume using simple XML (see `resume/example.xml`) that
   captures your work experience in well-worded bullet points describing every
   significant aspect of what you did.

2. When it comes time to apply for a job, remove irrelevant content, leaving
   only the details that speak directly to what the job posting asks for, saving
   the result as `resume/resume.xml`.

3. If you save the XML as `resume/resume.xml`, you can also just run `make` (or
   `make all`) to generate `resume/resume.tex` and `resume/resume.pdf`.

    For arbitrarily named resume file `resume/myresume.xml`, use make targets of
    `resume/myresume.tex` and `resume/myresume.pdf`, depending on what format
    you want.

    Without make, you would run `python3 stitch_resume.py resume/<yourfile>.xml`,
    which compiles the XML into a LaTeX file with the same name
    (`<yourfile>.tex` in this example) and in the same directory. Then run
    `pdflatex resume/<yourfile>.tex` to produce the PDF.

4. Review the resulting PDF, and make necessary adjustments, and recompile (step
   #3) as needed. Since both the Python script and the LaTeX class are
   lightweight, the compilation should be very quick.

## Resume XML Format

Stitchjob resumes are authored in a lightweight XML format that balances structure with flexibility. The XML file must begin with a `<resume>` root element and typically includes the following:

- `<contact>`: Your name, email, phone, location, and optional links (e.g., GitHub, LinkedIn).
- `<section>`: Major sections of the resume (e.g., Summary, Key Competencies, Experience, Education). Use the `heading` attribute to specify a title; optionally, add a `type` for semantic grouping.
- `<skills>`: Inside a section, lists individual `<skill>` elements.
- `<experience>`: Work or project entries, with attributes `begin` and `end`. Child elements include `<title>`, `<organization>`, `<location>`, optional `<blurb>`, and a list of `<item>` bullet points or freeform text `<description>`.
- `<degree>`: For education, including `<date>`, `<type>`, `<field>`, `<school>`, and `<location>`.

The format is intentionally minimal and easy to edit. See [`resume/example.xml`](resume/example.xml) for a complete, working example. Or just jump in by copying [`resume/template.xml`](resume/template.xml) and filling in your details.

## Directory Structure

```
stitchjob/
├── CHANGELOG.md        # Log of major changes
├── LICENSE             # Text of the MIT License
├── Makefile            # Build script for PDF generation
├── stitch_resume.py    # Python script to convert XML to LaTeX
├── README.md           # This file
└── resume/             # Resume .XML, .TEX, and .PDF files
  ├── example.xml       # Example resume
  ├── example.tex       # Generated from example.xml
  ├── example.pdf       # Compiled from example.tex
  └── stitched.cls      # LaTeX resume class for Stitchjob resumes
```
