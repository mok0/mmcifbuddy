SHELL=/bin/sh

all: mmciflexermodule.so wheel

PHONY: mmciflexermodule.so
mmciflexermodule.so:
	cd src && $(MAKE) install

.PHONY: wheel mmciflexermodule.so
wheel: clean-build-env README.md
	python3 -m build

README.md: README.org
	pandoc -f org -t gfm $< -o $@

.PHONY: clean
clean:
	@$(RM) *~

.PHONY: clean-build-env
clean-build-env:
	@find . -name *.egg-info -exec rm -rf {} +
	@$(RM) -r build/

.PHONY: clean-cache
clean-cache:
	@find . -name *.pyc -exec rm -rf {} +

.PHONY: veryclean
veryclean: clean clean-cache clean-build-env
