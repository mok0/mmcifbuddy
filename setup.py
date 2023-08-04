import subprocess
from setuptools import setup, Extension


subprocess.run(["python3", "update_version.py"], cwd="./src")

ext_module = Extension('mmcifreader.mmciflexer._mmciflexer',
                    sources = ['src/mmciflexermodule.c', 'src/lex.mmcif.c'],
                    include_dirs = ['src/'],
                    language="c",
                    libraries=[])

setup(ext_modules=[ext_module])
