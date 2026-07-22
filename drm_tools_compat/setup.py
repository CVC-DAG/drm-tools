from setuptools import setup, find_packages

setup(
    name="drm-tools",
    version="1.0.0a1",
    description="Deprecated: use cvcdocdb instead. This package is a compatibility shim.",
    author="Oriol Ramos Terrades",
    author_email="oriolrt@cvc.uab.cat",
    url="https://github.com/CVC-DAG/cvcdocdb",
    license="MIT",
    packages=find_packages(),
    install_requires=["cvcdocdb>=1.0.0a1"],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Deprecated :: This package is deprecated. Use cvcdocdb instead.",
    ],
)
