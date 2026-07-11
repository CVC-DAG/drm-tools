from setuptools import setup, find_packages
import os

NAME = "drm"
VERSION = "1.1.0"
DESCR = "Package for document representation model"
URL = "https://github.com/CVC-DAG/drm-tools"

AUTHOR = """Oriol Ramos Terrades
Jialuo Chen
Adrià Molina
"""
EMAIL = "{oriolrt, jchen, amolina}@cvc.uab.cat"

LICENSE = "MIT License"

SRC_DIR = {"drm"}
PACKAGES = find_packages(exclude='drm/')

def get_long_description():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    return ""

def get_requirements():
    reqs = []
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                # Skip empty lines and lines that are not actual package names (e.g. -rtd-theme)
                if line and not line.startswith("-") and not line.startswith("#"):
                    reqs.append(line)
    return reqs

setup(name=NAME,
    version=VERSION,
    description=DESCR,
    long_description_content_type="text/markdown",
    long_description=get_long_description(),
    author_email=EMAIL,
    author=AUTHOR,
    url=URL,
    license=LICENSE,
    package_dir={},
    packages=PACKAGES,
    install_requires=get_requirements(),
    keywords=['python', "documents", "classification", "knowledge representation","neo4j"],
    classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Operating System :: Unix",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
      ]
    )