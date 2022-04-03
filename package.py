# -*- coding: utf-8 -*-

name = 'ic_ui'

version = '3.0.0-beta'

description = 'UI-related modules'

authors = ['mjbonnington']

requires = [
	# 'duperlogger', 
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
	alias('style-test', 'python {root}/style_test.py')
