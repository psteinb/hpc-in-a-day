SRC_FILES?=$(wildcard *md)
DST_FILES=$(SRC_FILES:%.md=%.pdf)
PANDOC_FLAGS?=
PANDOC_APP?=pandoc


all : $(DST_FILES)

%.pdf : %.md
	$(PANDOC_APP) $(PANDOC_FLAGS) -o $@ $^

clean :
	@rm -vf $(DST_FILES)
