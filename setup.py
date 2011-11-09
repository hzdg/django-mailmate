from setuptools import setup, find_packages
import emailtools

setup(
    name='Email Tools',
    version='.'.join(map(str, emailtools.__version__)),
    author='Chris McKenzie',
    author_email='chrismc@hzdg.com',
    packages=find_packages(),
    include_package_data=False,
    description='Django email tools.',
    license='LICENSE.txt',
    url='http://gitorious.hzdesign.com/django-emailtools/django-emailtools',
    long_description=open('README').read(),
    zip_safe = False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)