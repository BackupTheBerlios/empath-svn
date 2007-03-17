# Module: template
# File: template.py
# Copyright (C) 2006 Ariel De Ocampo arieldeocampo@gmail.com
#
# This module is part of the <WHAT-HAVE-YOU> project and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from setuptools import setup, find_packages

setup(
  name="SkeletonEgg",
  version="0.0.1",
  description="""SkeletonEgg""",
  author="Ariel De Ocampo",
  author_email = 'arieldeocampo@gmail.com',
  license = 'MIT',


#  entry_points="""
#  [entry.point.name]
#  ext-name = __name__.somemod:SomeCallable
#  """

#  package_data={'testme': ['data/somefile.dat']},

  packages=find_packages('src'),
  package_dir={'': 'src'}
)

