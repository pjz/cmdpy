from distribute_setup import use_setuptools
use_setuptools()

from setuptools import find_packages, setup
version = open('version.txt').read()


classifiers = [ 'Development Status :: 4 - Beta'
              , 'Environment :: Console'
              , 'Intended Audience :: Developers'
              , 'License :: OSI Approved :: MIT'
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
     , packages = find_packages(exclude=['cmdpy.tests', 'cmdpy.tests.*'])
     , py_modules = []
     , url = 'http://github.com/pjz/cmdpy'
     , version = version
     , zip_safe = False
      )

