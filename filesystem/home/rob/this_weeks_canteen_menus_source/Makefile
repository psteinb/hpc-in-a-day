SRC_FILES?=$(wildcard *md)
DST_FILES=$(SRC_FILES:%.md=%.pdf)
PANDOC_FLAGS?=
PANDOC_APP?=pandoc


all : $(DST_FILES)

%.pdf : %.md
	$(PANDOC_APP) $(PANDOC_FLAGS) -o $@ $^

install : $(DST_FILES)
	@mkdir -p ../this_weeks_canteen_menus
	@cp -v $^ ../this_weeks_canteen_menus

clean :
	@rm -vf $(DST_FILES)

help :
	@echo "all     : translate all markdown files in the current folder to .pdf using pandoc"
	@echo "install : create folder ../this_weeks_canteen_menus and copy all .pdfs there (rebuild them if needed)"
	@echo "clean   : remove all pdfs in this folder"
