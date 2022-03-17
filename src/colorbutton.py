import math
import os

from Qt import QtCore, QtGui, QtWidgets


_blank_msg = ""


class ColorButton(QtWidgets.QPushButton):
	"""Colour picker button class. Inherits QPushButton."""

	# Create a signal to emit when the image is changed
	color_changed = QtCore.Signal()

	def __init__(self, parent=None):
		super(ImageButton, self).__init__(parent)

		self.setProperty('colorChooser', True)
		self.setAcceptDrops(True)
		self.setToolTip(_blank_msg)
		self.setStyleSheet("QPushButton { background-color: %s }" % value)


	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore()


	def dragMoveEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore()


	def dropEvent(self, e):
		"""Event handler for files dropped on to the widget."""

		if e.mimeData().hasUrls:
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
			for url in e.mimeData().urls():
				fname = str(url.toLocalFile())

			# print("Dropped '%s' on to widget." % fname)
			if os.path.isfile(fname):
				if os.path.splitext(fname)[1] in _allowed_formats:
					self.updateThumbnail(fname)
		else:
			e.ignore()
