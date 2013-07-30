import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


pkgmeta = {}
execfile(os.path.join(os.path.dirname(__file__),
         'mailmate', 'pkgmeta.py'), pkgmeta)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '-s']
        self.test_suite = True

    def run_tests(self):
        import pytest
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='django-mailmate',
    version='.'.join(map(str, pkgmeta['__version__'])),
    author='Chris McKenzie',
    author_email='chrismc@hzdg.com',
    packages=find_packages(),
    include_package_data=False,
    description='Django email tools.',
    license='LICENSE.txt',
    url='http://github.com/hzdg/django-mailmate',
    long_description=open('README.rst').read(),
    zip_safe = False,
    tests_require=[
        'pytest-django',
    ],
    install_requires=[
        'Django>=1.2',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    cmdclass={'test': PyTest},
)
