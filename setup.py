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
     , description = 'Dopy is a library to take the pain out of writing commandline tools'
     , name = 'dopy'
     , packages = find_packages(exclude=['dopy.tests', 'dopy.tests.*'])
     , py_modules = []
     , url = 'http://github.com/pjz/dopy'
     , version = version
     , zip_safe = False
      )

