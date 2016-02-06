#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='liscript',
    version='0.0.1',
    description='lisp dialect',
    url='https://github.com/KolesnichenkoDS/liscript',
    author='Daniil Kolesnichenko',
    author_email='d.s.kolesnichenko@ya.ru',
    license='MIT',

    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages('liscript', 'liscript.*'),

    entry_points={
        'console_scripts': [
            'lirepl=liscript:repl',
            'lirun=liscript:compile',
        ],
    },
)
