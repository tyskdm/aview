
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

.PHONY: all clean doc doc-clean puml-img puml-clean test test-cov spec-cov spec-clean

all: clean db

# clean: db-clean puml-clean doc-clean spec-clean 
clean: db-clean
	@py3clean .

#
# AUTOSAR C++14 Guidelines
#

db:
	@mkdir -p $(ASDBDIR)/17-10
	@mkdir -p $(ASDBDIR)/19-03

	@pdftotext -f 18 -l 300 \
		$(ASDBDIR)/pdf/17-10/AUTOSAR_RS_CPP14Guidelines.pdf \
		$(ASDBDIR)/17-10/AUTOSAR_RS_CPP14Guidelines.txt
	@aview conv -i $(ASDBDIR)/17-10/AUTOSAR_RS_CPP14Guidelines.txt \
		> $(ASDBDIR)/17-10/[17-10]_C++14_Coding_Rules.txt

	@pdftotext -f 21 -l 386 \
		$(ASDBDIR)/pdf/19-03/AUTOSAR_RS_CPP14Guidelines.pdf \
		$(ASDBDIR)/19-03/AUTOSAR_RS_CPP14Guidelines.txt
	@aview conv -i $(ASDBDIR)/19-03/AUTOSAR_RS_CPP14Guidelines.txt \
		> $(ASDBDIR)/19-03/[19-03]_C++14_Coding_Rules.txt

db-clean:
	@$(RM) -rf $(ASDBDIR)/17-10
	@$(RM) -rf $(ASDBDIR)/19-03

db-install:
	@mkdir -p $(ASDBDIR)/pdf/17-10
	curl https://www.autosar.org/fileadmin/user_upload/standards/adaptive/17-10/AUTOSAR_RS_CPP14Guidelines.pdf \
		-o $(ASDBDIR)/pdf/17-10/AUTOSAR_RS_CPP14Guidelines.pdf
	@mkdir -p $(ASDBDIR)/pdf/19-03
	curl https://www.autosar.org/fileadmin/user_upload/standards/adaptive/21-11/AUTOSAR_RS_CPP14Guidelines.pdf \
		-o $(ASDBDIR)/pdf/19-03/AUTOSAR_RS_CPP14Guidelines.pdf

db-remove:
	@$(RM) -rf $(ASDBDIR)

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
