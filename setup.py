## -*- encoding: utf-8 -*-
"""Testing binder services for deploying mini form-based web services for earth sciences
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='test-binder',
    version='0.1.0',
    description='Testing binder services for deploying mini form-based web services for earth sciences',
    long_description=long_description,
    url='https://github.com/nthiery/test-binder',
    author='Tamir Kamai and Nicolas M. Thiéry',
    author_email='nthiery@users.sf.net',
    license='GPLv2+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 3',
    ],
    keywords='binder jupyter',
    py_modules=find_packages(),
    setup_requires=['pytest-runner'],
    install_requires=['scipy', 'matplotlib', 'pandas', 'jupyter'],
    tests_require=['pytest'],
)
