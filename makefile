BIBTEX   = bibtex
PDFTEX = pdflatex -interaction=nonstopmode -halt-on-error -shell-escape

.PHONY: all

ALLSRC := dguest_vr-jet-bump.tex
all: $(ALLSRC:.tex=.pdf)
	@rm -f TMP-*

TEXFILES := $(shell find -L . -name '*.tex')
FIGURES := $(shell find -L figures/ -name '*.pdf')
FIGURES += figures/spec.pdf

$(FIGURES): code/plot_vr_bump.py
	@echo "remaking figures"
	@./code/plot_vr_bump.py

%.bbl: %.tex $(TEXFILES) *.bib
	$(PDFTEX) dguest_vr-jet-bump.tex --draftmode
	$(BIBTEX) dguest_vr-jet-bump.tex

IGNORE_WARNINGS := 'Marginpar on page|float specifier changed'
COLOR_WARNINGS := '^LaTeX Warning:|Fatal error'
FILTER_WARN := egrep -v $(IGNORE_WARNINGS) | egrep --color $(COLOR_WARNINGS)
%.pdf: %.tex $(TEXFILES) $(FIGURES)
	$(PDFTEX) $< --draftmode
	$(PDFTEX) $<
