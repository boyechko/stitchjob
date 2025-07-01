# Resumoid

**Resumoid** is a lightweight toolchain for generating LaTeX resumes from
semantically structured XML. It allows you to write your resume as clean,
readable XML and render it into a polished PDF using a custom LaTeX class.

---

## Features

- Write your resume in **semantic XML** --- clean, structured, and version-controllable
- Transform it into a **LaTeX resume** via a modular Python script
- Use a custom LaTeX class (`rb-resume.cls`) for formatting control
- Automate the build process with a Makefile
- Easily extendable to support multiple outputs (HTML, Markdown, etc.)

---

## Directory Structure

```
xml-resume/
├── resume.xml # Main resume content (semantic XML)
├── xmlresume.py # Python script to convert XML to LaTeX
├── rb-resume.cls # Custom LaTeX resume class
├── Makefile # Build script for PDF generation
├── tests/
│ └── sample.xml # Sample resume data for testing
└── README.md # This file
```

## Usage

### Generate LaTeX:

```bash
python3 xmlresume.py resume.xml -o resume.tex
```

### Build PDF:

```bash
make
```

### Clean build artifacts:

```bash
make clean
```
