SHELL = /bin/sh

#INCLUDEPY = -I/usr/local/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/include/python3.11
INCLUDEPY := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['INCLUDEPY'])")
#PY_CFLAGS= -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX10.15.sdk
PY_CFLAGS := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['PY_CFLAGS'])")
#LDSHARED = -bundle -undefined dynamic_lookup -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX10.15.sdk
LDSHARED := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['LDSHARED'][6:])")
#EXT_SUFFIX = .cpython-311-darwin.so
EXT_SUFFIX := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['EXT_SUFFIX'])")
MMCIFLEXERMODULE := mmciflexermodule$(EXT_SUFFIX)
LOCAL_INSTALL_DIR := ../mmcifreader/mmciflexer

.PHONY: all
all: $(MMCIFLEXERMODULE) test_mmcif_lex test_strtok_r test_enum 

install: build
	install $(MMCIFLEXERMODULE) $(LOCAL_INSTALL_DIR)

$(MMCIFLEXERMODULE): mmciflexermodule.o lex.mmcif.o 
	clang $(LDSHARED) $^ -o $@

mmciflexermodule.o: mmciflexermodule.c mmciflexer.h
	$(CC) -c $(PY_CFLAGS) -I$(INCLUDEPY) $< -o $@

lex.mmcif.o: lex.mmcif.c 
	$(CC) -c $(PY_CFLAGS) $< -o $@

lex.mmcif.c: mmcif.lex mmciflexer.h
	$(LEX) mmcif.lex

test_mmcif_lex: test_mmcif_lex.o lex.mmcif.c
	$(CC) $^ -o $@

test_enum: test_enum.o
	$(CC) $^ -o $@

test_strtok_r: test_strtok_r.o
	$(CC) $^ -o $@

.PHONY: clean
clean:
	$(RM)  *.o *~
	$(RM)  *.so lex.mmcif.c mmcif_test *~ lex.yy.c

.PHONY: veryclean
veryclean: clean
	$(RM) mmciflexermodule$(EXT_SUFFIX)
