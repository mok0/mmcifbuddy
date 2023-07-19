# $Id: Makefile,v 1.5 2000/08/17 23:14:19 mok Exp $

SHELL=/bin/sh

all:	mmciflexmodule.so mmcif_test

mmciflexmodule.so: lex.yy.c mmciflexmodule.c
	python3 -m build --wheel

lex.yy.c: mmcif.lex
	$(LEX) mmcif.lex

mmcif_test: mmcif_test.o lex.yy.o
	$(CC) $^ -o $@

.PHONY:	clean veryclean mmciflexmodule.so

clean:
	$(RM)  *.o

veryclean: clean
	$(RM)  *.so lex.yy.c mmcif_test *~
	$(RM) -r build/

#  Local Variables:
#  mode: makefile
#  End:
