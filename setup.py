#!/usr/bin/env python3
"""
Setup script for ARM Stack Usage Analyzer

This script configures the package for installation via pip, making the
arm-stack tool available as a command-line utility.
"""

from setuptools import setup, find_packages
import os
import re

# Read version from the main script
def get_version():
    with open('arm-stack', 'r', encoding='utf-8') as f:
        content = f.read()
        version_match = re.search(r'__version__ = ["\']([^"\']*)["\']', content)
        if version_match:
            return version_match.group(1)
    raise RuntimeError('Unable to find version string')

# Long description for PyPI
def get_long_description():
    return """
A comprehensive Python tool for analyzing stack usage in ARM embedded projects. 
Parses object files and stack usage data to build complete call graphs and calculate 
peak memory consumption. Features include color-coded reports, JSON export, build 
comparison, and support for both standard (.o) and Zephyr/CMake (.c.obj) object files.
    """.strip()

setup(
    name='arm-stack-analyzer',
    version=get_version(),
    author='wizath',
    author_email='',
    description='A comprehensive tool for analyzing stack usage in ARM embedded projects',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/wizath/arm-stack',
    project_urls={
        'Bug Reports': 'https://github.com/wizath/arm-stack/issues',
        'Source': 'https://github.com/wizath/arm-stack',
        'Changelog': 'https://github.com/wizath/arm-stack/blob/main/CHANGELOG.md',
    },
    scripts=['arm-stack'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Debuggers',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    keywords='arm embedded stack analysis memory firmware objdump',
    python_requires='>=3.6',
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
) 
 