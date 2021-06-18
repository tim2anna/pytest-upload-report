#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-upload-report',
    version='0.1.0',
    author='Anna',
    author_email='191996155@qq.com',
    maintainer='Anna',
    maintainer_email='191996155@qq.com',
    license='MIT',
    url='https://github.com/tim2anna/pytest-upload-report',
    description='pytest-upload-report is a plugin for pytest that upload your test report for test results.',
    long_description_content_type="text/x-rst",
    long_description=read('README.rst'),
    packages=["pytest_upload_report"],
    keywords="py.test pytest report allure upload",
    python_requires='>=3.7',
    install_requires=['pytest>=6.2.4', 'requests>=2.25.1', 'allure-pytest>=2.9.43', 'pytest-html>=3.1.1'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'upload_report = pytest_upload_report.plugin',
        ],
    },
)
