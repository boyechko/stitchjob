# Patchworker

**Patchworker** is a plaintext-first toolchain for assembling custom-fit resumes
from modular parts. Rather than rewriting or cloning past resumes, Patchworker
encourages thoughtful tailoring by letting you trim, stitch, and combine
prewritten bullet points into job-specific documents.

Built for writers, developers, and anyone tired of one-size-fits-all job applications.

## Requirements

- Python 3.7+
- LaTeX installation with `pdflatex`
- Make (optional, for automated builds)

## General Process

1. Create a master resume using simple XML (see `resume/sample.xml`) that
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

    Without make, you would run `python3 patchworker.py resume/<yourfile>.xml`,
    which compiles the XML into a LaTeX file with the same name
    (`<yourfile>.tex` in this example) and in the same directory. Then run
    `pdflatex resume/<yourfile>.tex` to produce the PDF.

4. Review the resulting PDF, and make necessary adjustments, and recompile (step
   #3) as needed. Since both the Python script and the LaTeX class are
   lightweight, the compilation should be very quick.

## Directory Structure

```
patchworker/
├── CHANGELOG.md        # Log of major changes
├── LICENSE             # Text of the MIT License
├── Makefile            # Build script for PDF generation
├── patchworker.py      # Python script to convert XML to LaTeX
├── patchworker.cls     # LaTeX resume class
├── resume/             # Resume .XML, .TEX, and .PDF files
├── README.md           # This file
├── resume.xml          # Main resume content (semantic XML)
└── sample.xml          # Sample resume data for testing
```

