#!/usr/bin/python

# popup.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2021
#
# Pop-up message dialog
# Can be used to display a brief help or information message which requires no
# user action and can be dismissed with a click.


import os

from Qt import QtCore, QtGui, QtWidgets


# class ClosePopupFilter(QtCore.QObject):
# 	""" """
# 
# 	def eventFilter(self, target, event):
# 		if event.type() == QtCore.QEvent.WindowDeactivate:
# 			target.close()
# 		return False


class PopupDialog(QtWidgets.QDialog):
	"""Main dialog class."""

	def __init__(self, parent=None):
		super(PopupDialog, self).__init__(parent)

		self.parent = parent

		# self.__popup_filter = ClosePopupFilter()
		# self.installEventFilter(self.__popup_filter)

		# Set window icon, flags and other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Setup window and UI widgets
		self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
		# self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
		self.setSizeGripEnabled(False)
		# self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		# self.setStyleSheet("background: transparent;")
		self.setStyleSheet("background: rgb(252,152,103); color: #000;")

		self.message_label = QtWidgets.QLabel(self)
		self.message_label.setWordWrap(True)
		# self.message_label.setStyleSheet("border-radius: 6px; background: rgb(252,152,103); color: #000;")

		vbox = QtWidgets.QVBoxLayout()
		vbox.addStretch(1)
		vbox.addWidget(self.message_label)
		self.setLayout(vbox)


	def display(self, message="", attachTo=None):
		"""Display message in popup dialog.

		The message can be attached to a QWidget with 'attachTo'.
		"""
		if message:
			self.message_label.setText(message)

		if attachTo:  # Attach popup to a widget
			# gp = attachTo.mapToGlobal(QtCore.QPoint(0, 0))
			gp = attachTo.mapToGlobal(attachTo.rect().bottomLeft())
			# print(gp)
			self.move(gp)
		else:  # Move to centre of parent window
			self.move(self.parent.frameGeometry().center() - self.frameGeometry().center())

		self.exec_()  # Make the dialog modal


	def mousePressEvent(self, QMouseEvent):
		"""Close about dialog if mouse is clicked."""

		self.accept()
