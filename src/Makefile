
# building 'mmciflexer' extension
# clang -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX10.15.sdk -I/private/var/folders/69/j1sbdfkd6bv6mctm27rd26fc0000gn/T/build-env-yl8vlswv/include -I/usr/local/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/include/python3.11 -c lex.mmcif.c -o build/temp.macosx-10.15-x86_64-cpython-311/lex.mmcif.o


SHELL=/bin/sh

python_includes := $(shell python3-config --includes)
python_cflags := $(shell python3-config --cflags)
python_ldflags := $(shell python3-config --ldflags)

all:	test_mmcif_lex test_strtok_r test_enum 

PHONY: build
build: mmciflexermodule.so
	

mmciflexermodule.so: mmciflexermodule.c lex.mmcif.c mmciflexer.h
	gcc $(python_cflags) $(python_includes) $(python_ldflags) $< -o $@

lex.mmcif.c: mmcif.lex
	$(LEX) mmcif.lex

test_mmcif_lex: test_mmcif_lex.o lex.mmcif.o
	$(CC) $^ -o $@

test_enum: test_enum.o
	$(CC) $^ -o $@

test_strtok_r: test_strtok_r.o
	$(CC) $^ -o $@

.PHONY: clean
clean:
	$(RM)  *.o *~
	$(RM)  *.so lex.mmcif.c mmcif_test *~ lex.yy.c
