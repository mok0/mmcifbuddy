
from setuptools import setup, Extension

ext_module = Extension('mmcifreader.mmciflexer._mmciflexer',
                    sources = ['src/mmciflexermodule.c', 'src/lex.mmcif.c'],
                    include_dirs = ['src/'],
                    language="c",
                    libraries=[])

setup(ext_modules=[ext_module])
