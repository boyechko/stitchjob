# Patchworker

**Patchworker** is a plaintext-first toolchain for assembling custom-fit resumes
from modular parts. Rather than rewriting or cloning past resumes, Patchworker
encourages thoughtful tailoring by letting you trim, stitch, and combine
prewritten bullet points into job-specific documents.

Built for writers, developers, and anyone tired of one-size-fits-all job applications.

## Highlights

- Author once in structured XML
- Compile to clean LaTeX using Python
- Output polished PDFs tailored to each role
- Emphasizes modularity, reuse, and customization

## Directory Structure

```
xml-resume/
├── resume.xml # Main resume content (semantic XML)
├── patchworker.py # Python script to convert XML to LaTeX
├── patchworker.cls # LaTeX resume class
├── Makefile # Build script for PDF generation
├── output/ # Contains LaTeX and PDF files
│ ├── resume.tex # Compiled from resume.xml
│ └── resume.pdf # Compiled from resume.tex
├── tests/
│ └── sample.xml # Sample resume data for testing
└── README.md # This file
```

## General Process

1. Create a master resume using simple XML (see `tests/sample.xml`) that
   captures your work experience in well-worded bullet points describing every
   significant aspect of what you did.

2. When it comes time to apply for a job, remote irrelevant content, leaving
   only the details that speak directly to what the job posting asks for, saving
   the result as `resume.xml` in the project's root directory.

3. If you save the XML as `resume.xml`, you can also just run `make` that
   generates `resume.tex` and `resume.pdf` in the `output/` subdirectory.

   To use custom names, run `python3 patchworker.py <yourfile>.xml`, which
   compiles the XML into a LaTeX file with the same name (`<yourfile>.tex` in
   this example). Then run `pdflatex output/<yourfile>.tex` to produce the PDF.

4. Review the resulting PDF, and make necessary adjustments, and recompile (step
   #3) as needed. Since both the Python script and the LaTeX class are
   lightweight, the compilation is nigh seamless.
