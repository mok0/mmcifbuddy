SHELL=/bin/sh

all:	mmciflexermodule.so test_mmcif_lex test_strtok_r test_enum

PHONY: mmflexermodule.so
mmciflexermodule.so: lex.mmcif.c mmciflexermodule.c
	python3 -m build --wheel
	python3 updateversion.py mmcifreader/__init__.py

lex.mmcif.c: mmcif.lex
	$(LEX) mmcif.lex

test_mmcif_lex: test_mmcif_lex.o lex.mmcif.o
	$(CC) $^ -o $@

test_enum: test_enum.o
	$(CC) $^ -o $@

test_strtok_r: test_strtok_r.o
	$(CC) $^ -o $@

.PHONY: clean-cache
clean-cache:
	@find . -name *.egg-info -exec rm -rf {} +
	@find . -name *.pyc -exec rm -rf {} +
	@find . -name *.pyo -exec rm -rf {} +
	@find . -name *.so -exec rm -rf {} +
	@find . -name *.pyd -exec rm -rf {} +

.PHONY: clean
clean:
	$(RM)  *.o *~

.PHONY: veryclean
veryclean: clean-cache clean
	$(RM)  *.so lex.mmcif.c mmcif_test *~ lex.yy.c
	$(RM) -r build/
	$(RM) -r dist/
