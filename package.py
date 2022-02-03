# -*- coding: utf-8 -*-

name = 'ic_ui'

version = '2.0.4'

description = 'UI-related modules'

authors = ['mjbonnington']

requires = [
    'python-2.7+', 
    'PySide2', 
]

build_requires = [
    'rezlib', 
]

build_command = 'python -m build {install}'


def commands():
    env.PYTHONPATH.append('{root}')
    env.IC_ICONPATH.append('{root}/icons')
