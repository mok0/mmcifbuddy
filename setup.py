from setuptools import setup, Extension

ext_module = Extension('mmcifbuddy.mmciflexer._mmciflexer',
                       sources = ['src/mmciflexermodule.c',
                                  'src/lex.mmcif.c',
                                  'src/sneaky_fopen.c'],
                        depends = ['Makefile',
                                   'README.org',
                                   'src/Makefile',
                                   'src/version.h',
                                   'src/mmciflexer.h',
                                   'src/mmcif.lex',
                                   'test/4af1.cif',
                                   'test/semicolon.cif',
                                   'test/chem_comp.cif',
                                   'test/two_datablocks.cif',
                                   ],
                       language="c",
                       libraries=['z'])

setup(ext_modules=[ext_module])
