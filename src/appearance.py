import os
import platform
# from pprint import pprint

from Qt import QtCore, QtGui, QtWidgets


class Appearance(QtCore.QObject):
	"""Appearance class.

	Manage custom UI colour palette and stylesheet.
	"""

	col = {}
	stylesheet = ""
	color_changed = QtCore.Signal()

	def __init__(self, widget, qss=None):
		"""Class constructor.

		Arguments:
			widget (QObject) - Apply styles to this widget/window.
			qss (str) - File path to QSS stylesheet file.
		"""
		super(Appearance, self).__init__()
		self.widget = widget
		self.qss = qss

		# Store some system UI colours & define colour palette ---------------
		self.col['text'] = QtGui.QColor(204, 204, 204)
		self.col['disabled'] = QtGui.QColor(102, 102, 102)
		self.col['highlighted-text'] = QtGui.QColor(255, 255, 255)
		self.col['sys-window'] = QtWidgets.QWidget().palette().color(QtGui.QPalette.Window)
		self.col['sys-highlight'] = QtWidgets.QWidget().palette().color(QtGui.QPalette.Highlight)

		self.col['window'] = self.col['sys-window']  # Use base window color from OS / parent app
		# self.col['window'] = QtGui.QColor('#444444')  # Standard dark grey
		# self.col['window'] = QtGui.QColor('#33393b')  # Adwaita dark #2b3032

		self.col['highlight'] = self.col['sys-highlight']  # Use highlight color from OS / parent app
		# self.col['highlight'] = QtGui.QColor('#78909c')

		self.computeUIPalette()

		# Load and set stylesheet --------------------------------------------
		if qss is not None:
			self.read_stylesheet()

		# Set up keyboard shortcuts ------------------------------------------
		self.shortcutClearQSS = QtWidgets.QShortcut(self.widget)
		self.shortcutClearQSS.setKey('Ctrl+Shift+R')
		self.shortcutClearQSS.activated.connect(self.clear_stylesheet)

		self.shortcutReloadQSS = QtWidgets.QShortcut(self.widget)
		self.shortcutReloadQSS.setKey('Ctrl+R')
		self.shortcutReloadQSS.activated.connect(self.read_stylesheet)

		self.shortcutCycleStyles = QtWidgets.QShortcut(self.widget)
		self.shortcutCycleStyles.setKey('Ctrl+Alt+R')
		self.shortcutCycleStyles.activated.connect(self.cycle_styles)

		# End initialisation -------------------------------------------------


	def color_picker_dialog(self, current_color=None):
		"""Display a system dialog for choosing a colour.

		Return the selected colour as a QColor object, or None if the dialog
		is cancelled.
		"""

		color_dialog = QtWidgets.QColorDialog()
		color_dialog.setOption(QtWidgets.QColorDialog.DontUseNativeDialog)  # Set with kwarg?

		# Set current colour
		if current_color is not None:
			color_dialog.setCurrentColor(current_color)

		# Only return a color if valid / dialog accepted
		if color_dialog.exec_() == color_dialog.Accepted:
			color = color_dialog.selectedColor()
			return color


	def cycle_styles(self):
		"""Cycle through preset Qt styles and apply application-wide."""

		try:
			style = next(self.styles)
		except (AttributeError, NameError, StopIteration):
			self.styles = iter(QtWidgets.QStyleFactory.keys())
			style = next(self.styles)

		self.set_qt_style(style)


	def set_qt_style(self, style):
		"""Apply preset Qt style."""

		self.clear_stylesheet()
		QtWidgets.QApplication.setStyle(style)
		print("Set style to '%s'" % style)


	def clear_stylesheet(self):
		"""Clear stylesheet."""

		self.stylesheet = ""
		self.widget.setStyleSheet(self.stylesheet)


	def read_stylesheet(self):  #, input_qss):
		"""Read stylesheet.

		Arguments:
			input_qss (str) - Input path from which to read QSS file.
		"""
		with open(self.qss, 'r') as fh:
			print("Read stylesheet: %s" % self.qss)
			self.stylesheet_orig = fh.read()
			self.apply_stylesheet(self.stylesheet_orig)


	def apply_stylesheet(self, stylesheet):
		"""Process the dynamic stylesheet and apply to widget."""

		# Read predefined colour variables and apply them to the style
		for key, value in self.col.items():
			rgb = "%d, %d, %d" % (value.red(), value.green(), value.blue())
			stylesheet = stylesheet.replace(r"%{}%".format(key), rgb)

		# Replace image theme tokens
		stylesheet = stylesheet.replace(r"%theme%", self.imgtheme)

		# Replace font tokens
		font_str = ""
		# if HOST != 'houdini':
		if platform.system() == 'Windows':
			font_str = "'Segoe UI'"
		elif platform.system() == 'Linux':
			font_str = "'Cantarell', 'OpenSans', 'sans'"
		stylesheet = stylesheet.replace(r"%systemfont%", font_str)

		self.stylesheet = stylesheet
		self.widget.setStyleSheet(self.stylesheet)


	def write_stylesheet(self, output_qss):
		"""Write stylesheet and bake tokens for compatibility.

		Arguments:
			output_qss (str) - Output path to write QSS file.
		"""
		with open(output_qss, 'w') as fh:
			fh.write("/* Generated by uistyle */\n")
			fh.write(self.stylesheet)


	def color_offset(self, input_color, amount, clamp=None):
		"""Lighten or darken input_color by a given amount.

		Arguments:
			input_color (QColor) - Input colour to adjust.
			amount (int) - Value to offset +/- 255.
			clamp (int, optional) - Value between 0-255. The output lightness
				is not allowed to go past this min/max value.
		"""
		if amount == 0:  # Do nothing
			return input_color

		elif amount > 0:  # Lighten
			if clamp is None:
				min_clamp = 0
			else:
				min_clamp = clamp
			max_clamp = 255

		elif amount < 0:  # Darken
			min_clamp = 0
			if clamp is None:
				max_clamp = 255
			else:
				max_clamp = clamp

		lum = max(min_clamp, min(input_color.lightness()+amount, max_clamp))
		h, s, l, a = input_color.getHsl()
		out_color = QtGui.QColor()
		out_color.setHsl(h, s, lum)
		return out_color


	def computeUIPalette(self):
		"""Compute complementary UI colours based on window colour."""

		# self.col['group-bg'] = QtGui.QColor(128, 128, 128)
		self.col['line'] = self.col['window'].darker(110)
		self.col['tooltip'] = QtGui.QColor(17, 17, 17)
		self.col['mandatory'] = QtGui.QColor(252, 152, 103)
		self.col['warning'] = QtGui.QColor(255, 216, 106)
		self.col['inherited'] = QtGui.QColor(161, 239, 228)
		self.col['group-bg'] = self.col['window'].lighter(110)

		if self.col['window'].lightness() < 128:  # Dark UI
			self.imgtheme = "light"
			self.col['text'] = QtGui.QColor(204, 204, 204)
			# self.col['group-bg'] = QtGui.QColor(0, 0, 0)
			self.col['disabled'] = QtGui.QColor(102, 102, 102)
			# self.col['disabled'] = self.color_offset(self.col['window'], +51)
			# self.col['base'] = self.color_offset(self.col['window'], -34, 34)
			# self.col['alternate'] = self.color_offset(self.col['base'], +6)
			# self.col['button-border'] = self.color_offset(self.col['button'], +8)
			# self.col['menu-bg'] = self.color_offset(self.col['window'], -17, 68)
			# self.col['menu-border'] = self.color_offset(self.col['menu-bg'], +17)
			# self.col['group-header'] = self.color_offset(self.col['window'], +17)
			self.col['base'] = self.col['window'].darker(150)
			self.col['alternate'] = self.col['base'].lighter(105)
			# self.col['button'] = self.col['window'].lighter(150)
			self.col['button'] = self.color_offset(self.col['window'], +34)
			self.col['button-border'] = self.col['button']
			self.col['menu-bg'] = self.col['window'].darker(125)
			self.col['menu-border'] = self.col['menu-bg'].lighter(150)
			self.col['group-header'] = self.col['window'].lighter(150)
			self.col['hover'] = self.col['button'].lighter(110)
		else:  # Light UI
			self.imgtheme = "dark"
			self.col['text'] = QtGui.QColor(51, 51, 51)
			# self.col['group-bg'] = QtGui.QColor(255, 255, 255)
			self.col['disabled'] = QtGui.QColor(102, 102, 102)
			# self.col['disabled'] = self.color_offset(self.col['window'], -51)
			# self.col['base'] = self.color_offset(self.col['window'], +34, 221)
			# self.col['alternate'] = self.color_offset(self.col['base'], -6)
			# self.col['button-border'] = self.color_offset(self.col['button'], -8)
			# self.col['menu-border'] = self.color_offset(self.col['menu-bg'], -17)
			# self.col['group-header'] = self.color_offset(self.col['window'], -17)
			self.col['base'] = self.col['window'].lighter(105)
			self.col['alternate'] = self.col['base'].darker(105)
			# self.col['button'] = QtGui.QColor("#eee")
			# self.col['button'] = self.col['window'].darker(110)
			self.col['button'] = self.color_offset(self.col['window'], -17)
			self.col['button-border'] = self.col['button'].darker(125)
			# self.col['menu-bg'] = self.col['window'].darker(110)
			self.col['menu-bg'] = self.color_offset(self.col['window'], +17)
			self.col['menu-border'] = self.col['menu-bg'].darker(150)
			self.col['group-header'] = self.col['window'].darker(110)
			self.col['hover'] = self.col['button'].lighter(110)

		# self.col['hover'] = self.color_offset(self.col['button'], +17)
		# self.col['checked'] = self.color_offset(self.col['button'], -17)
		# self.col['hover'] = self.col['button'].lighter(110)
		self.col['checked'] = self.col['highlight'].lighter(225)  # tint
		self.col['pressed'] = self.col['button'].darker(110)

		if self.col['highlight'].lightness() < 136:
			self.col['highlighted-text'] = QtGui.QColor(255, 255, 255)
		else:
			self.col['highlighted-text'] = QtGui.QColor(0, 0, 0)

		if self.col['tooltip'].lightness() < 136:
			self.col['tooltip-text'] = QtGui.QColor(255, 255, 255)
		else:
			self.col['tooltip-text'] = QtGui.QColor(0, 0, 0)

		# if self.col['button'].lightness() < 170:
		# 	self.col['button-text'] = self.color_offset(self.col['button'], +68, 204)
		# else:
		# 	self.col['button-text'] = self.color_offset(self.col['button'], -68, 51)
		self.col['button-text'] = self.col['text']

		self.col['mandatory-bg'] = self.col['mandatory']
		if self.col['mandatory-bg'].lightness() < 128:
			self.col['mandatory-text'] = self.color_offset(self.col['mandatory-bg'], +68, 204)
		else:
			self.col['mandatory-text'] = self.color_offset(self.col['mandatory-bg'], -68, 51)

		self.col['warning-bg'] = self.col['warning']
		if self.col['warning-bg'].lightness() < 128:
			self.col['warning-text'] = self.color_offset(self.col['warning-bg'], +68, 204)
		else:
			self.col['warning-text'] = self.color_offset(self.col['warning-bg'], -68, 51)

		self.col['inherited-bg'] = self.col['inherited']
		if self.col['inherited-bg'].lightness() < 128:
			self.col['inherited-text'] = self.color_offset(self.col['inherited-bg'], +68, 204)
		else:
			self.col['inherited-text'] = self.color_offset(self.col['inherited-bg'], -68, 51)


	@QtCore.Slot(int)
	def setUIBrightness(self, value):
		"""Set the UI style background shade."""

		# print(value)
		h, s, l, a = self.col['window'].getHsl()
		self.col['window'].setHsl(h, s, value)
		# self.col['window'] = QtGui.QColor(value, value, value)
		self.computeUIPalette()
		self.apply_stylesheet(self.stylesheet_orig)


	# @QtCore.Slot()
	def setUIColor(self, role, color=None):
		"""Set the UI style colour for the given role."""

		widget = self.widget.sender()

		# Get current colour and pass to function
		current_color = widget.palette().color(QtGui.QPalette.Background)
		color = self.color_picker_dialog(current_color)
		if color:
			widget.setStyleSheet("QWidget { background-color: %s }" % color.name())
			self.col[role] = color
			self.computeUIPalette()
			self.apply_stylesheet(self.stylesheet_orig)
			self.color_changed.emit()


	# # @QtCore.Slot()
	# def store_color(self):
	# 	"""Get the colour from a dialog opened from a colour chooser button.
	# 	"""
	# 	widget = self.sender()

	# 	# Get current colour and pass to function
	# 	current_color = widget.palette().color(QtGui.QPalette.Background)
	# 	color = self.color_picker_dialog(current_color)
	# 	if color:
	# 		widget.setStyleSheet("QWidget { background-color: %s }" % color.name())
	# 		category, attr = self.getWidgetMeta(self.sender())
	# 		self.storeValue(category, attr, color.name())