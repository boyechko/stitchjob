PYTHON = python3
LATEX = pdflatex

all: resume.tex output/resume.pdf

resume.tex: resume.xml xmlresume.py rb-resume.cls
	$(PYTHON) xmlresume.py resume.xml -o resume.tex

output/resume.pdf: resume.tex
	mkdir -p output
	$(LATEX) -output-directory=output resume.tex

clean:
	rm -f resume.tex output/*
