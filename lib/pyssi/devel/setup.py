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
        Extension("pyssi._speedups.core", ["src/pyssi/_speedups/core.pyx"]),
        Extension("pyssi._speedups.util", ["src/pyssi/_speedups/util.pyx"]),
    ]
)

setup(
    name="PySSI",
    version="0.0.1",
    description="""Python signal slot implementation""",
    author="Ariel De Ocampo",
    author_email = 'arieldeocampo@gmail.com',
    license = 'MIT',


#  entry_points="""
#  [entry.point.name]
#  ext-name = __name__.somemod:SomeCallable
#  """

#  package_data={'testme': ['data/somefile.dat']},

    packages=find_packages('src'),
    package_dir={'': 'src'},
    features={'speedups': speedups},
)

