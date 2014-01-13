import os
import sys
import os.path
from optparse import make_option
from fabricate import main, run, shell, autoclean

# Core Executables
# ================

name = 'dopy'

RUN_DEPS = [ ]

TEST_DEPS = [ 'coverage', 'pytest' ]

def _virt(cmd, envdir='env'):
    return os.path.join(envdir, 'bin', cmd)

ENV_ARGS = [
            './vendor/virtualenv-1.7.1.2.py',
            '--distribute',
            '--unzip-setuptools',
            '--prompt=[%s] ' % name,
            '--extra-search-dir=./vendor/',
            ]

def dev():
    if os.path.exists('env'): return
    args = [ main.options.python ] + ENV_ARGS + [ 'env' ]
    run(*args)

    for dep in RUN_DEPS + TEST_DEPS:
        run(_virt('pip'), 'install', '--no-use-wheel', dep)
    run(_virt('python'), 'setup.py', 'develop')

def clean_dev():
    shell('rm', '-rf', 'env')

def clean():
    autoclean()
    shell('find', '.', '-name', '*.pyc', '-delete')
    clean_dev()
    clean_test()
    clean_build()

# Testing
# =======

def test():
    dev()
    run(_virt('py.test'), 'tests/', ignore_status=True, silent=False)

def analyse():
    dev()
    run(_virt('py.test'),
            '--junitxml=testresults.xml',
            '--cov-report', 'term',
            '--cov-report', 'xml',
            '--cov', name,
            'tests/',
            ignore_status=False)
    print('done!')

def clean_test():
    clean_dev()
    shell('rm', '-f', '.coverage', 'coverage.xml', 'testresults.xml', 'pylint.out')

# Build
# =====

def build():
    run(main.options.python, 'setup.py', 'bdist_egg')

def clean_build():
    shell(main.options.python, 'setup.py', 'clean', '-a')
    shell('rm', '-rf', 'dist')

def release():
    run()

def show_targets():
    print("""Valid targets:

    show_targets (default) - this
    build - build an egg
    dev - set up an environment able to run tests in env/
    test - run the unit tests
    pylint - run pylint on the source
    analyse - run the unit tests with code coverage enabled
    clean - remove all build artifacts
    clean_{dev,test} - clean some build artifacts

    """)
    sys.exit()

extra_options = [ make_option('--python', action="store", dest="python", default="python")
                , make_option('--release', action="store", dest="release", default=None)
                ]

main( extra_options=extra_options
    , default='show_targets'
    , ignoreprefix="python"
     )
