# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from setuptools import setup, find_packages, Feature, Extension

speedups = Feature(
    "optional C speed-enhancement modules",
    standard = True,
    ext_modules = [
        Extension("aossi._speedups.core", ["src/aossi/_speedups/core.pyx"]),
        Extension("aossi._speedups.cwrapper", ["src/aossi/_speedups/cwrapper.pyx"]),
        Extension("aossi._speedups.util", ["src/aossi/_speedups/util.pyx"]),
    ]
)

setup(
    name="aossi",
    version="0.4.0-1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    features={'speedups': speedups},

#    package_data={'aossi_docs': 'data/somefile.dat'},

    # Metadata
    description="""Signal-slot implementation""",
    author="Ariel De Ocampo",
    author_email = 'arieldeocampo@gmail.com',
    license = "MIT"
)

