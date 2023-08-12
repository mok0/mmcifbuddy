SHELL=/bin/sh

all: mmciflexermodule.so

PHONY: mmciflexermodule.so
mmciflexermodule.so:
	cd src && $(MAKE)

.PHONY: install
wheel: clean-build-env
	python3 updateversion.py mmcifbuddy/__init__.py
	python3 -m build --wheel

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
veryclean: clean-cache clean
	@$(RM) -r dist/
