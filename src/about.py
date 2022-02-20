#!/usr/bin/python

# about.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2015-2021
#
# Pop-up 'About' dialog / splash screen.


import os

from Qt import QtCore, QtGui, QtWidgets


class AboutDialog(QtWidgets.QDialog):
	"""Main dialog class."""

	def __init__(self, parent=None):
		super(AboutDialog, self).__init__(parent)

		# Setup window and UI widgets
		self.setWindowFlags(QtCore.Qt.Popup)

		self.resize(640, 288)
		self.setMinimumSize(QtCore.QSize(640, 288))
		self.setMaximumSize(QtCore.QSize(640, 288))
		self.setSizeGripEnabled(False)

		self.bg_label = QtWidgets.QLabel(self)
		self.bg_label.setGeometry(QtCore.QRect(0, 0, 640, 288))

		self.message_label = QtWidgets.QLabel(self)
		self.message_label.setGeometry(QtCore.QRect(16, 16, 608, 256))
		self.message_label.setStyleSheet("background: transparent; color: #FFF;")
		self.message_label.setWordWrap(True)

		self.icon_label = QtWidgets.QLabel(self)
		self.icon_label.setGeometry(QtCore.QRect(0, 0, 256, 256))

		# Add dropshadow to text
		effect = QtWidgets.QGraphicsDropShadowEffect()
		effect.setColor(QtGui.QColor(0, 0, 0))
		effect.setOffset(1, 1)
		effect.setBlurRadius(2)
		self.message_label.setGraphicsEffect(effect)


	def display(self, 
		background=None, 
		icon_pixmap=None, 
		message=""):
		"""Display message in about dialog.

		Keyword Arguments:
			background (QColor or str): QColor object, or path to an image
				file to use for the background.
			icon_pixmap (QPixmap): Foreground image or icon.
			message (str): Text message to display.
		"""
		if isinstance(background, QtGui.QColor):
			self.bg_label.setStyleSheet("background: %s" % background.name())

		elif isinstance(background, str):
			pixmap = QtGui.QPixmap(background)
			self.bg_label.setPixmap(pixmap.scaled(
				self.bg_label.size(), QtCore.Qt.KeepAspectRatioByExpanding, 
				QtCore.Qt.SmoothTransformation))
			self.bg_label.setAlignment(QtCore.Qt.AlignCenter)

		if icon_pixmap:
			# Offset message from centre to make space for icon
			# TODO: take icon size into account
			self.message_label.setGeometry(QtCore.QRect(288, 16, 336, 256))

			self.icon_label = QtWidgets.QLabel(self)
			self.icon_label.setGeometry(QtCore.QRect(16, 16, 256, 256))
			self.icon_label.setPixmap(icon_pixmap.scaled(
				self.icon_label.size(), QtCore.Qt.KeepAspectRatio, 
				QtCore.Qt.SmoothTransformation))
			self.icon_label.setAlignment(QtCore.Qt.AlignCenter)

		if message:
			self.message_label.setText(message)

		# Move to centre of active screen
		desktop = QtWidgets.QApplication.desktop()
		screen = desktop.screenNumber(desktop.cursor().pos())
		self.move(desktop.screenGeometry(screen).center() - self.frameGeometry().center())

		self.exec_()  # Make the dialog modal


	def mousePressEvent(self, QMouseEvent):
		"""Close about dialog if mouse is clicked."""

		self.accept()
