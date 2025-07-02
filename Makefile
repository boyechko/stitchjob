PYTHON = python3
LATEX = pdflatex
SCRIPT = patchworker.py
CLS = patchworker.cls

all: output/resume.tex output/resume.pdf

output/%.tex: %.xml $(SCRIPT) $(CLS)
	echo "Building $@ from $<"
	mkdir -p output
	$(PYTHON) $(SCRIPT) $< -o $@

output/%.pdf: output/%.tex %.xml
	echo "Building $@ from $<"
	$(LATEX) -output-directory=output $<

clean:
	rm -f output/*
