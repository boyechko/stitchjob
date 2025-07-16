PYTHON = python3
LATEX = pdflatex

all: resume letter

clean:
	cd $(RESUME_DIR) && find . -type f | sed 's|^\./||' | egrep -v -f .clean-keep | xargs -r rm --
	cd $(LETTER_DIR) && find . -type f | sed 's|^\./||' | egrep -v -f .clean-keep | xargs -r rm --

# Resume

RESUME_SCRIPT = stitchjob/stitch_resume.py
RESUME_CLS = stitchjob/stitched.cls
RESUME_DIR = resume
RESUME_NAME = resume

.SECONDARY: $(RESUME_DIR)/%.tex
.PRECIOUS: $(RESUME_DIR)/%.tex $(RESUME_DIR)/%.pdf

resume: $(RESUME_DIR)/$(RESUME_NAME).tex $(RESUME_DIR)/$(RESUME_NAME).pdf

$(RESUME_DIR)/%.tex: $(RESUME_DIR)/%.xml $(RESUME_SCRIPT) $(RESUME_CLS)
	$(PYTHON) $(RESUME_SCRIPT) $<

$(RESUME_DIR)/%.pdf: $(RESUME_DIR)/%.tex $(RESUME_DIR)/%.xml
	$(LATEX) -output-directory=$(RESUME_DIR) $<

# Letter

LETTER_SCRIPT = stitchjob/stitch_letter.py
LETTER_TEMPLATE = stitchjob/letter.mako
LETTER_DIR = letter
LETTER_NAME = letter

.SECONDARY: $(LETTER_DIR)/%.tex
.PRECIOUS: $(LETTER_DIR)/%.tex $(LETTER_DIR)/%.pdf

letter: $(LETTER_DIR)/$(LETTER_NAME).tex $(LETTER_DIR)/$(LETTER_NAME).pdf

$(LETTER_DIR)/%.tex: $(LETTER_DIR)/%.md $(LETTER_SCRIPT) $(LETTER_TEMPLATE)
	$(PYTHON) $(LETTER_SCRIPT) $< -r $(RESUME_DIR)/$(RESUME_NAME).xml

$(LETTER_DIR)/%.pdf: $(LETTER_DIR)/%.md $(LETTER_DIR)/%.tex
	$(PYTHON) $(LETTER_SCRIPT) $< -r $(RESUME_DIR)/$(RESUME_NAME).xml -p
