PYTHON = python3
LATEX = pdflatex

all: output/resume.tex output/resume.pdf

output/resume.tex: resume.xml patchworker.py patchworker.cls
	$(PYTHON) patchworker.py resume.xml -o output/resume.tex

output/resume.pdf: output/resume.tex
	mkdir -p output
	$(LATEX) -output-directory=output resume.tex

clean:
	rm -f resume.tex output/*
