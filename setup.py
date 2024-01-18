"""Setup for pygruenbeck_cloud python package."""
from __future__ import annotations

from os import path

from setuptools import find_packages, setup

PACKAGE_NAME = "pygruenbeck_cloud"
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

VERSION = {}
# pylint: disable=exec-used
with open(path.join(HERE, PACKAGE_NAME, "__version__.py"), encoding="utf-8") as fp:
    exec(fp.read(), VERSION)

PACKAGES = find_packages(exclude=["tests", "tests.*", "dist", "build"])

REQUIRES = ["aiohttp>=3.8.1"]

setup(
    name=PACKAGE_NAME,
    version=VERSION["__version__"],
    license="MIT License",
    url="https://github.com/p0l0/pygruenbeck_cloud",
    download_url="https://github.com/p0l0/pygruenbeck_cloud/tarball/"
    + VERSION["__version__"],
    author="Marco Neumann",
    author_email="pygruenbeck_cloud@binware.dev",
    description="Python Library to communicate with Grünbeck Cloud based Water softeners",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=PACKAGES,
    package_data={"pygruenbeck_cloud": ["py.typed"]},
    zip_safe=False,
    platforms="any",
    python_requires=">=3.11",
    install_requires=REQUIRES,
    keywords=["gruenbeck", "gruenbeck-cloud", "home", "automation"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Home Automation",
    ],
)
