# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

### Fixed

## [0.1.0] - 2025-08-14

### Added

- `stitch_letter.py` to generate cover letters from Markdown input:
  - `closing` and `signature` fields in letter metadata.
  - `signature_image` via metadata or CLI (`-S`).
- Unified CLI subcommand interface `stitch`:
  - `letter` subcommand to generate cover letters from Markdown.
  - `resume` subcommand to generate resumes from XML.
  - `-p/--pdf` and `-P/--openpdf` for compiling and opening PDFs.
  - `--verbose` command line argument.
- Produced PDFs are well-tagged and accessible.
- Sample letter and resume files:
  - `resume/example.xml`, `.tex`, `.pdf`
  - `letter/example.md`, `example_signature.png`, `.tex`, `.pdf`
- New elements for `resume.xml`:
  - `<skills>...</skills>` to contain individual `<skill>` elements.
  - `<section>...</section>` element in place of specialized sections.
  - `<description>` element.
- `resume.dtd`, `resume.rnc`, and `schemas.xml` to support validation.
- Basic unit tests for resume and letter processing.

### Changed

- Rename the project to Stitchjob, playing on having a "tailored" job materials.
- Major changes to `stitched.cls` resume class:
  + `\datedsection` became `\experience`.
  + `\degree` items now wrapped in `education` environment.
- All resume inputs and outputs now reside in `resume/`.
- Signature image specified in letter input file is added even without `-s`
  command-line argument.
- Parser reads all children of `<resume>...</resume>` element in order, allowing
  order of the sections in the XML to carry into the output.
- User profile information gets spread over two lines if too much for one.

### Fixed

- Properly escape LaTeX-sensitive characters while preserving math and formatting symbols.
- Visibly mark links in `stitched.cls`.
- Ensure `stitched.cls` is findable by `pdflatex`.
- Correct rendering of small caps section headings in resume.
- Strip protocol (`https://`) from website contact field.

## [0.0.1] - 2025-06-29

### Added

- Created the project.
