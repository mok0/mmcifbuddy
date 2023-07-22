from setuptools import setup, Extension

ext_module = Extension('mmciflexer._mmciflexer',
                    sources = ['src/mmciflexermodule.c', 'src/lex.mmcif.c'],
                    language="c",
                    libraries=[])

setup(ext_modules=[ext_module])
