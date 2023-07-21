from setuptools import setup, Extension

module1 = Extension('mmciflexer',
                    sources = ['src/mmciflexermodule.c', 'src/lex.mmcif.c'],
                    language="c",
                    libraries=[])

setup(ext_modules=[module1])
