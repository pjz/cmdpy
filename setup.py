from distribute_setup import use_setuptools
use_setuptools()

from setuptools import find_packages, setup

classifiers = [ 'Development Status :: 4 - Beta'
              , 'Environment :: Console'
              , 'Intended Audience :: Developers'
              , 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
              , 'Natural Language :: English'
              , 'Operating System :: MacOS :: MacOS X'
              , 'Operating System :: Microsoft :: Windows'
              , 'Operating System :: POSIX'
              , 'Programming Language :: Python :: 2.7'
              , 'Programming Language :: Python :: Implementation :: CPython'
              , 'Topic :: Software Development :: Libraries :: Application Frameworks'
              ]

setup( author = 'Paul Jimenez'
     , author_email = 'pj@place.org'
     , classifiers = classifiers
     , description = 'Cmdpy is a library to take the rote scutwork out of writing commandline tools in python'
     , name = 'cmdpy'
     , py_modules = [ 'distribute_setup', 'cmdpy' ]
     , url = 'http://github.com/pjz/cmdpy'
     # there must be nothing on the following line after the = other than a string constant 
     , version = '1.4-dev'
     , zip_safe = False
      )

