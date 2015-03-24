MMARK = mmark
XML2RFC = xml2rfc

all: rfc-dnscomp.txt
clean:
	rm -f *.xml *.txt

%.xml: %.md
	$(MMARK) -xml2 -page $< > $@
%.txt: %.xml
	$(XML2RFC) --text $<

.PHONY: all clean
