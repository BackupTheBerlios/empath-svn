# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from setuptools import setup, find_packages

setup(
    name="aossi",
    version="0.3.1-1",
    packages=find_packages('src'),
    package_dir={'': 'src'},

#    package_data={'aossi_docs': 'data/somefile.dat'},

    # Metadata
    description="""Signal-slot implementation""",
    author="Ariel De Ocampo",
    author_email = 'arieldeocampo@gmail.com',
    license = "MIT"
)

