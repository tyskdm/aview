
TARGET      := gdoc

# directories
SRCDIR 		:= gdoc
SPECDIR     := spec
TESTDIR     := tests
DOXYGENDIR  := doxy
DOXYOUTDIR  := html
DOXYXMLDIR  := xml
PYTESTDIR   := htmlcov
ASDBDIR 	:= database

all: clean db

# clean: db-clean puml-clean doc-clean spec-clean 
clean: db-clean
	@py3clean .

#
# AUTOSAR C++14 Guidelines
#

db:
	@mkdir -p $(ASDBDIR)/A1710
	@mkdir -p $(ASDBDIR)/A1903

	@pdftotext -f 18 -l 300 \
		$(ASDBDIR)/pdf/A1710/AUTOSAR_RS_CPP14Guidelines.pdf \
		$(ASDBDIR)/A1710/AUTOSAR_RS_CPP14Guidelines.txt
	@aview conv -i $(ASDBDIR)/A1710/AUTOSAR_RS_CPP14Guidelines.txt -t text \
		> $(ASDBDIR)/A1710/[17-10]_C++14_Coding_Rules.txt
	@aview conv -i $(ASDBDIR)/A1710/AUTOSAR_RS_CPP14Guidelines.txt -t json \
		> $(ASDBDIR)/A1710/[17-10]_C++14_Coding_Rules.json

	@pdftotext -f 21 -l 386 \
		$(ASDBDIR)/pdf/A1903/AUTOSAR_RS_CPP14Guidelines.pdf \
		$(ASDBDIR)/A1903/AUTOSAR_RS_CPP14Guidelines.txt
	@aview conv -i $(ASDBDIR)/A1903/AUTOSAR_RS_CPP14Guidelines.txt -t text \
		> $(ASDBDIR)/A1903/[19-03]_C++14_Coding_Rules.txt
	@aview conv -i $(ASDBDIR)/A1903/AUTOSAR_RS_CPP14Guidelines.txt -t json \
		> $(ASDBDIR)/A1903/[19-03]_C++14_Coding_Rules.json

db-clean:
	@$(RM) -rf $(ASDBDIR)/A1710
	@$(RM) -rf $(ASDBDIR)/A1903

pdf-install:
	@mkdir -p $(ASDBDIR)/pdf/A1710
	curl https://www.autosar.org/fileadmin/user_upload/standards/adaptive/17-10/AUTOSAR_RS_CPP14Guidelines.pdf \
		-o $(ASDBDIR)/pdf/A1710/AUTOSAR_RS_CPP14Guidelines.pdf
	@mkdir -p $(ASDBDIR)/pdf/A1903
	curl https://www.autosar.org/fileadmin/user_upload/standards/adaptive/21-11/AUTOSAR_RS_CPP14Guidelines.pdf \
		-o $(ASDBDIR)/pdf/A1903/AUTOSAR_RS_CPP14Guidelines.pdf

pdf-remove:
	@$(RM) -rf $(ASDBDIR)/pdf

#
# Doxygen
#
DOXYGENFLAGS :=

doc:
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYOUTDIR)
	@cd doxy/; doxygen $(DOXYGENFLAGS)

doc-clean:
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYOUTDIR)
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYXMLDIR)

#
# PlantUML
#
PUMLSRC   := .
PUMLFLAGS :=

puml-img:
	@find $(PUMLSRC) \( -name *.puml -or -name *.pu \) | while read line; \
    do \
		echo puml-img: $$line; \
	 	dir=$${line%.*}; \
		dir=$$(basename "$$dir"); \
		plantuml -o "./_puml_/$$dir" $$PUMLFLAGS "$$line"; \
	done

puml-clean:
	@find $(PUMLSRC) \( -name *.puml -or -name *.pu \) | while read line; \
    do \
	 	dir=$${line%.*}; \
		parent_dir=$$(dirname "$$dir"); \
		$(RM) -rf "$$parent_dir"/_puml_; \
	done

#
# pytest
#
PYTESTFLAGS :=

test:
	@pytest $(PYTESTFLAGS)

test-cov:
	@pytest $(PYTESTFLAGS) --cov $(SRCDIR) --cov-branch

spec-cov:
	@pytest $(SPECDIR) $(PYTESTFLAGS) --cov $(SRCDIR) --cov-branch --cov-report=html

spec-clean:
	@$(RM) -rf $(PYTESTDIR)

.PHONY: all clean doc doc-clean puml-img puml-clean test test-cov spec-cov spec-clean pdf-install pdf-remove
