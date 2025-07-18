# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Add `--verbose` command line argument.
- Add unified CLI subcommand interface `stitch` rather than using individual scripts.
- Add `stitch_letter.py` to generate cover letters from Markdown input.
- Add command-line options `-p/--pdf`, `-s`, and `-S` for compiling PDFs and
  including signature images in letters.
- Include `letter/example.md`, `example.tex`, and `example.pdf` as sample letter files.
- Add support for `closing` and `signature` fields in letter metadata.
- Add support for relative `signature_image` path via metadata or CLI.
- Include `resume.rnc` and `schemas.xml` to support validation against Relax NG Compact schema.
- Add `resume.dtd` for DTD-based validation.
- Add `Contact` class and validation of contact fields for resume output.
- Include basic unit tests for resume and letter processing.
- Introduce `<skills>...</skills>` to contain individual `<skill>` elements.
- Introduce `<description>` element.

### Changed

- Signature image specified in letter input file is added even without `-s`
  command-line argument.
- Include only contact information mentioned in the XML file.
- Rename the project to Stitchjob, playing on having a "tailored" job materials.
- All resume inputs and outputs now reside in `resume/`.
- Add `resume/example.xml` along with its LaTeX and PDF outputs.
- Parser reads all children of `<resume>...</resume>` element in order, allowing
  order of the sections in the XML to carry into the output.
- Introduce `<section>...</section>` element in place of specialized sections.
- User profile information gets spread over two lines if too much for one.

### Fixed

- Ensure `stitched.cls` is findable by `pdflatex`.
- Correct rendering of small caps section headings in resume.
- Strip protocol (`https://`) from website contact field.
- Properly escape LaTeX-sensitive characters while preserving math and formatting symbols.

## [0.0.1] - 2025-06-29

### Added

- Created the project.
