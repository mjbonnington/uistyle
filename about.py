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

		self.resize(640, 320)
		self.setMinimumSize(QtCore.QSize(640, 320))
		self.setMaximumSize(QtCore.QSize(640, 320))
		self.setSizeGripEnabled(False)

		self.bg_label = QtWidgets.QLabel(self)
		self.bg_label.setGeometry(QtCore.QRect(0, 0, 640, 320))

		self.message_label = QtWidgets.QLabel(self)
		self.message_label.setGeometry(QtCore.QRect(16, 16, 608, 288))
		self.message_label.setStyleSheet("background: transparent; color: #FFF;")

		self.icon_label = QtWidgets.QLabel(self)
		self.icon_label.setGeometry(QtCore.QRect(0, 0, 256, 256))

		# Add dropshadow to text
		effect = QtWidgets.QGraphicsDropShadowEffect()
		effect.setColor(QtGui.QColor(0, 0, 0))
		effect.setOffset(1, 1)
		effect.setBlurRadius(2)
		self.message_label.setGraphicsEffect(effect)


	def display(self, 
		bg_image=None, 
		bg_color=None, 
		icon_pixmap=None, 
		message=""):
		"""Display message in about dialog.

		Keyword arguments:
		bg_image - path to an image file to use for the background.
		bg_color - QColor object to use for the background colour, if bg_image
			is not set.
		icon_pixmap - QPixmap to use bor foreground image or icon.
		message - text message to display.
		"""
		if bg_image:
			pixmap = QtGui.QPixmap(bg_image)
			self.bg_label.setPixmap(pixmap.scaled(
				self.bg_label.size(), QtCore.Qt.KeepAspectRatioByExpanding, 
				QtCore.Qt.SmoothTransformation))
			self.bg_label.setAlignment(QtCore.Qt.AlignCenter)

		elif bg_color:
			self.bg_label.setStyleSheet("background: %s" % bg_color.name())

		if icon_pixmap:
			# Offset message from centre to make space for icon
			self.message_label.setGeometry(QtCore.QRect(256, 16, 368, 288))

			self.icon_label = QtWidgets.QLabel(self)
			self.icon_label.setGeometry(QtCore.QRect(0, 32, 256, 256))
			self.icon_label.setPixmap(icon_pixmap)

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
