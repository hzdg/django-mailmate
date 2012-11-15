from setuptools import setup, find_packages


setup(
    name='django-emailtools',
    version=':versiontools:emailtools:',
    author='Chris McKenzie',
    author_email='chrismc@hzdg.com',
    packages=find_packages(),
    include_package_data=False,
    description='Django email tools.',
    license='LICENSE.txt',
    url='http://github.com/hzdg/django-emailtools',
    long_description=open('README.rst').read(),
    zip_safe = False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    setup_requires=[
        'Django>=1.2',
        'versiontools >= 1.8',
    ]
)