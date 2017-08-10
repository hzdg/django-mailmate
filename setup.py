import os
from setuptools import setup, find_packages, Command
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
        # Make sure this package's tests module gets priority.
        sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
        errno = pytest.main(self.test_args)
        sys.exit(errno)


class LintCommand(Command):
    """
    A copy of flake8's Flake8Command

    """
    description = "Run flake8 on modules registered in setuptools"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def distribution_files(self):
        if self.distribution.packages:
            for package in self.distribution.packages:
                yield package.replace(".", os.path.sep)

        if self.distribution.py_modules:
            for filename in self.distribution.py_modules:
                yield "%s.py" % filename

    def run(self):
        from flake8.engine import get_style_guide
        flake8_style = get_style_guide(config_file='setup.cfg')
        paths = self.distribution_files()
        report = flake8_style.check_files(paths)
        raise SystemExit(report.total_errors > 0)


setup(
    name='django-mailmate',
    version=pkgmeta['__version__'],
    author='Chris McKenzie',
    author_email='chrismc@hzdg.com',
    packages=find_packages(),
    include_package_data=False,
    description='Django email tools.',
    license='MIT',
    url='http://github.com/hzdg/django-mailmate',
    long_description=open('README.rst').read(),
    zip_safe=False,
    setup_requires=[],
    tests_require=[
        'pytest-django==2.6',
        'markdownify',
        'flake8',
    ],
    install_requires=[
        'Django>=1.2',
    ],
    extras_require={
        'autoplaintext': [
            'markdownify',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    cmdclass={
        'test': PyTest,
        'lint': LintCommand,
    },
)
