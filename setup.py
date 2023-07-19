from setuptools import setup, Extension

module1 = Extension('mmciflex',
                    sources = ['mmciflexmodule.c', 'lex.yy.c'],
                    language="c",
                    libraries=[])

setup(ext_modules=[module1])
