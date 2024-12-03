from setuptools import setup, find_packages
from distutils.extension import Extension
import os
import codecs

NAME = "drm"
VERSION = "1.0"
DESCR = "Package for document representation model"
URL = "https://github.com/CVC-DAG/drm-tools"
#REQUIRES = ['numpy','cython','Image','matplotlib','IPython']

AUTHOR = """Oriol Ramos Terrades
Jialuo Chen
Adrià Molina
"""
EMAIL = "{oriolrt, jchen, amolina}@cvc.uab.cat"

LICENSE = "MIT License"

SRC_DIR = {"drm"}
PACKAGES = find_packages(exclude='drm/')

with codecs.open(os.path.join(  os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8") as fh:
  long_description = "\n" + fh.read()

with codecs.open(os.path.join(  os.path.abspath(os.path.dirname(__file__)), "requirements.txt"), encoding="utf-8") as fh:
  REQUIRES = fh.read().splitlines()

setup(name=NAME,
    version=VERSION,
    description=DESCR,
    long_description_content_type="text/markdown",
    long_description=long_description,
    requires=REQUIRES,
    author_email=EMAIL,
    author=AUTHOR,
    url=URL,
    license=LICENSE,
    package_dir={},
    packages=PACKAGES,
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],
    keywords=['python', "documents", "classification", "knowledge representation","neo4j"],
    classifiers=[
          "Development Status :: 1 - Planning",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3",
          "Operating System :: Unix",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
      ]
    )

