SHELL = /bin/sh

DATE=$(shell date -u +'%Y-%m-%d_%H:%M_%Z')
CC := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['CC'])")
INCLUDEPY := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['INCLUDEPY'])")
PY_CFLAGS := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['PY_CFLAGS'])")
CCSHARED := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['CCSHARED'])")
LDFLAGS := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['LDFLAGS'])")
LDSHARED := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['LDSHARED'])")
EXT_SUFFIX := $(shell python3 -c "import sysconfig; print(sysconfig.get_config_vars()['EXT_SUFFIX'])")

MMCIFLEXERMODULE := _mmciflexer$(EXT_SUFFIX)
LOCAL_INSTALL_DIR := ../mmcifbuddy/mmciflexer

.PHONY: all
all: $(MMCIFLEXERMODULE)

install: all
	install $(MMCIFLEXERMODULE) $(LOCAL_INSTALL_DIR)

# Parhaps on mac? check! clang $(LDSHARED) $^ -o $@

$(MMCIFLEXERMODULE): mmciflexermodule.o lex.mmcif.o sneaky_fopen.o
	$(LDSHARED) $^ -lz -o $@

mmciflexermodule.o: mmciflexermodule.c mmciflexer.h

	$(CC) -c $(PY_CFLAGS) $(CCSHARED) -I$(INCLUDEPY) -DCOMPILE_TIME=\"$(DATE)\" $< -o $@

lex.mmcif.o: lex.mmcif.c
	$(CC) -c $(PY_CFLAGS) $(CCSHARED) $< -o $@

sneaky_fopen.o: sneaky_fopen.c
	$(CC) -c $(PY_CFLAGS) $(CCSHARED)  $< -o $@

lex.mmcif.c: mmcif.lex mmciflexer.h
	$(LEX) mmcif.lex

test_mmcif_lex: test_mmcif_lex.c lex.mmcif.c
	$(CC) $^ -o $@

.PHONY: clean
clean:
	$(RM)  *.o *~
	$(RM)  *.so lex.mmcif.c mmcif_test lex.yy.c
	$(RM)	version.h

.PHONY: veryclean
veryclean: clean
	$(RM) mmciflexermodule$(EXT_SUFFIX)
