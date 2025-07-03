PYTHON = python3
LATEX = pdflatex
SCRIPT = stitch_resume.py
CLS = resume/stitched.cls

RESUME_DIR = resume
RESUME_NAME = resume

.SECONDARY: $(RESUME_DIR)/%.tex
.PRECIOUS: $(RESUME_DIR)/%.tex $(RESUME_DIR)/%.pdf

all: $(RESUME_DIR)/$(RESUME_NAME).tex $(RESUME_DIR)/$(RESUME_NAME).pdf

$(RESUME_DIR)/%.tex: $(RESUME_DIR)/%.xml $(SCRIPT) $(CLS)
	@echo "Building $@ from $<"
	$(PYTHON) $(SCRIPT) $< -o $@

$(RESUME_DIR)/%.pdf: $(RESUME_DIR)/%.tex $(RESUME_DIR)/%.xml
	@echo "Building $@ from $<"
	$(LATEX) -output-directory=$(RESUME_DIR) $<

clean:
	rm -f $(RESUME_DIR)/*.aux $(RESUME_DIR)/*.log $(RESUME_DIR)/*.out
