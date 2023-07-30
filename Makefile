SHELL=/bin/sh

all: mmciflexermodule.so 

PHONY: mmciflexermodule.so
mmciflexermodule.so: 
	cd src && $(MAKE)

.PHONY: install
install: 
	python3 updateversion.py mmcifreader/version.py
	python3 -m build --wheel

.PHONY: clean
clean:
	$(RM) *~

.PHONY: clean-cache
clean-cache:
	@find . -name *.egg-info -exec rm -rf {} +
	@find . -name *.pyc -exec rm -rf {} +

.PHONY: veryclean
veryclean: clean-cache clean
	$(RM) -r build/
	$(RM) -r dist/
