#from distutils.core import setup, Extension
from setuptools import setup, Extension
def main():

    module1 = Extension('mmciflex',
                        sources = ['mmciflexmodule.c', 'lex.yy.c'],
                        language="c",
                        libraries=[])

    setup(name="mmciflex",
          version="0.2.1",
          description="Python module to parse mmCIF file",
          author="Morten Kjeldgaard",
          author_email="mortenkjeldgaard@gmail.com",
          ext_modules=[module1]
          )

if __name__ == "__main__":
    main()
