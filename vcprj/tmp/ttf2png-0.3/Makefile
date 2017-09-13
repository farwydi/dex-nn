ttf2png: ttf2png.c
	gcc -Wall $^ -o $@ $(shell freetype-config --cflags --libs) $(shell pkg-config --cflags --libs libpng12)

VER=0.3

.PHONY: tarball
tarball: ttf2png-$(VER).tar.gz
ttf2png-$(VER).tar.gz: ttf2png.c Readme Makefile gpl.txt
	rm -rf ttf2png-$(VER)
	mkdir ttf2png-$(VER)
	cp -a $^ ttf2png-$(VER)
	tar -czf $@ ttf2png-$(VER)
	rm -rf ttf2png-$(VER)
