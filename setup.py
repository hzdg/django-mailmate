import os
from setuptools import setup, find_packages


pkgmeta = {}
execfile(os.path.join(os.path.dirname(__file__),
         'emailtools', 'pkgmeta.py'), pkgmeta)

setup(
    name='django-emailtools',
    version='.'.join(map(str, pkgmeta['__version__'])),
    author='Chris McKenzie',
    author_email='chrismc@hzdg.com',
    packages=find_packages(),
    include_package_data=False,
    description='Django email tools.',
    license='LICENSE.txt',
    url='http://github.com/hzdg/django-emailtools',
    long_description=open('README.rst').read(),
    zip_safe = False,
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
)
