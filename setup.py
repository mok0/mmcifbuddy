from setuptools import setup, Extension

module1 = Extension('mmciflexer',
                    sources = ['mmciflexermodule.c', 'lex.yy.c'],
                    language="c",
                    libraries=[])

setup(ext_modules=[module1])
