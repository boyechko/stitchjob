# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Changed

- Parser reads all children of <resume>...</resume> element in order, allowing
  order of the sections in the XML to carry into the output.
- Introduce <section>...</section> element in place of specialized sections.

### Added

- Introduce <skills>...</skills> to contain individual <skill> elements.
- Introduce <description> element.

## [0.0.1] - 2025-06-29

### Added

- Created the project.