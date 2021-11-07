# -*- coding: utf-8 -*-

name = 'ic_ui'

version = '1.0.0'

description = 'UI-related modules'

variants = [['python-3.9']]

requires = ['pyside2']

authors = ['mjbonnington']

build_command = 'python {root}/build.py {install}'


def commands():
    env.PYTHONPATH.append('{root}')
