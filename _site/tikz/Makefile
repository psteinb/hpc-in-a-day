

SRC_FILES=$(wildcard *tex)
SVG_FILES=$(SRC_FILES:.tex=.svg)
PDF_FILES=$(SRC_FILES:.tex=.pdf)

all : $(SVG_FILES) $(PDF_FILES)

%.pdf : %.tex
	pdflatex $< 

%.svg : %.pdf
	pdf2svg $< $@

clean:
	rm -rf *aux *log *svg *pdf
