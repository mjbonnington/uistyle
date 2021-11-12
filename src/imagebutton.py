#!/usr/bin/python

# shared/imagebutton.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2020-2021
#
# Image Button
# A special type of button to display and browse for an image. Supports drag-
# and-drop. Subclassed from QPushButton.


import math
import os

from Qt import QtCore, QtGui, QtWidgets


_blank_msg = "Browse, or drop image file here"
_allowed_formats = ['.png', '.jpg', '.gif', '.svg']


class ImageButton(QtWidgets.QPushButton):
	"""Image button class. Inherits QPushButton."""

	imageChanged = QtCore.Signal(str)

	def __init__(self, parent=None, max_size=[320, 320]):
		super(ImageButton, self).__init__(parent)

		self.maxSize = QtCore.QSize(max_size[0], max_size[1])
		# self.setFixedSize(self.maxSize)
		self.setStyleSheet("QWidget { width: %d; height: %d }" % (max_size[0], max_size[1]))

		self.setText("Drop image here")
		self.setToolTip(_blank_msg)
		self.setProperty('imageButton', True)
		self.setAcceptDrops(True)


	def updateThumbnail(self, image_path):
		"""Update thumbnail preview with image."""

		# print(image_path)
		if (image_path is not None) and \
			os.path.isfile(image_path):
			pixmap = QtGui.QPixmap(image_path)
			icon = QtGui.QIcon(pixmap)
			size = self.getImageSize(pixmap)
			self.setText("")
			self.setIcon(icon)
			# self.resize(size)
			self.setFixedSize(size)
			self.setIconSize(size)
			self.setStyleSheet("QWidget { padding: 0; min-width: 0; border: none; background: transparent }")
			self.imageChanged.emit(image_path)
		else:
			self.setText(_blank_msg)
			self.setStyleSheet("")


	def getImageSize(self, pixmap):
		"""Return the max resolution for an image."""

		max_w = self.maxSize.width()
		max_h = self.maxSize.height()
		w = pixmap.size().width()
		h = pixmap.size().height()
		ratio = float(w)/float(h)

		if w > max_w:
			w = max_w
			h = int(math.ceil(w/ratio))

		if h > max_h:
			h = max_h
			w = int(math.ceil(h*ratio))

		# print(w, h)
		return QtCore.QSize(w, h)


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
