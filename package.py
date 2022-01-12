# -*- coding: utf-8 -*-

name = 'ic_ui'

version = '2.0.2'

description = 'UI-related modules'

# variants = [['python-2.7+']]

requires = [
    'python-2.7+', 
    'PySide2'
]

authors = ['mjbonnington']

build_command = 'python {root}/build.py {install}'


def commands():
    env.PYTHONPATH.append('{root}')
    env.IC_ICONPATH.append('{root}/icons')
