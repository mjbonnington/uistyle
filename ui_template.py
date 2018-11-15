#!/usr/bin/python

# ui_template.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2018
#
# UI Template - a custom class to act as a template for all windows and
# dialogs.
# This module provides windowing / UI helper functions for better integration
# of PySide / PyQt UIs in supported DCC applications.
# Currently only Maya and Nuke are supported.


import os
import re

from Qt import QtCompat, QtCore, QtGui, QtWidgets
import rsc_rc  # Import resource file as generated by pyside-rcc

# Import custom modules
#import osOps
#import settingsData
#import userPrefs


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# The vendor string must be set in order to store window geometry
VENDOR = "UNIT"


# ----------------------------------------------------------------------------
# Main window class
# ----------------------------------------------------------------------------

class TemplateUI(object):
	""" Template UI class.

		Subclasses derived from this class need to also inherit QMainWindow or
		QDialog. This class has no __init__ constructor as a fudge to get
		around the idiosyncracies of multiple inheritance whilst retaining
		compatibility with both Python 2 and 3.
	"""
	def setupUI(self, 
		        window_object, 
		        window_title="", 
		        ui_file="", 
	            stylesheet="", 
	            xml_data="", 
	            store_window_geometry=True):
		""" Setup the UI.
		"""
		# Store some system UI colours & define colour palette
		tmpWidget = QtWidgets.QWidget()
		self.col = {}
		self.col['window'] = tmpWidget.palette().color(QtGui.QPalette.Window)
		self.col['highlight'] = tmpWidget.palette().color(QtGui.QPalette.Highlight)
		self.computeUIPalette()

		# info_str = "Window object: %s Parent: %s" %(self, self.parent)
		# print(info_str)

		# Define some global variables
		self.currentAttrStr = ""

		# Instantiate XML data class
		if xml_data:
			self.xd = settingsData.SettingsData()
			xd_load = self.xd.loadXML(xml_data)

		# Load UI & stylesheet
		if ui_file:
			#uifile = os.path.join(os.environ['IC_FORMSDIR'], ui_file)
			uifile = ui_file
			self.ui = QtCompat.loadUi(uifile, self)
		self.stylesheet = stylesheet
		self.loadStyleSheet()

		# Set window title
		self.setObjectName(window_object)
		if window_title:
			self.setWindowTitle(window_title)
		else:
			window_title = self.windowTitle()

		# Perform custom widget setup
		self.setupWidgets(self.ui)

		# Restore window geometry and state
		self.store_window_geometry = store_window_geometry
		if self.store_window_geometry:

			# Use QSettings to store window geometry and state.
			# (Restore state may cause issues with PyQt5)
			#if os.environ['IC_ENV'] == 'STANDALONE':
			print("Restoring window geometry for '%s'." %self.objectName())
			try:
				self.settings = QtCore.QSettings(VENDOR, window_title)
				self.restoreGeometry(self.settings.value("geometry", ""))
				# self.restoreState(self.settings.value("windowState", ""))
			except:
				pass

			# # Makes Maya perform magic which makes the window stay on top in
			# # OS X and Linux. As an added bonus, it'll make Maya remember the
			# # window position.
			# elif os.environ['IC_ENV'] == 'MAYA':
			# 	self.setProperty("saveWindowPref", True)

			# elif os.environ['IC_ENV'] == 'NUKE':
			# 	pass

		# else:
		# 	# Move to centre of active screen
		# 	desktop = QtWidgets.QApplication.desktop()
		# 	screen = desktop.screenNumber(desktop.cursor().pos())
		# 	self.move(desktop.screenGeometry(screen).center() - self.frameGeometry().center())
		# 	# Move to centre of parent window
		# 	self.move(self.parent.frameGeometry().center() - self.frameGeometry().center())

		# Set up keyboard shortcuts
		self.shortcutReloadStyleSheet = QtWidgets.QShortcut(self)
		self.shortcutReloadStyleSheet.setKey('Ctrl+Shift+R')
		self.shortcutReloadStyleSheet.activated.connect(self.loadStyleSheet)


	def fileDialog(self, startingDir, fileFilter='All files (*.*)'):
		""" Opens a dialog from which to select a single file.

			The env check puts the main window in the background so dialog pop
			up can return properly when running inside certain applications.
			The window flags bypass a Mac bug that made the dialog always
			appear under the Icarus window. This is ignored in a Linux env.
		"""
		envOverride = ['MAYA', 'NUKE']
		if os.environ['IC_ENV'] in envOverride:
			if os.environ['IC_RUNNING_OS'] == "MacOS":
				self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				self.show()
			dialog = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Files'), startingDir, fileFilter)
			if os.environ['IC_RUNNING_OS'] == "MacOS":
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				self.show()
		else:
			dialog = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Files'), startingDir, fileFilter)

		try:
			return dialog[0]
		except IndexError:
			return None


	def folderDialog(self, startingDir):
		""" Opens a dialog from which to select a folder.

			The env check puts the main window in the background so dialog pop
			up can return properly when running inside certain applications.
			The window flags bypass a Mac bug that made the dialog always
			appear under the Icarus window. This is ignored in a Linux env.
		"""
		envOverride = ['MAYA', 'NUKE']
		if os.environ['IC_ENV'] in envOverride:
			if os.environ['IC_RUNNING_OS'] == "MacOS":
				self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				self.show()
			dialog = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Directory'), startingDir, QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)
			if os.environ['IC_RUNNING_OS'] == "MacOS":
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				self.show()
		else:
			dialog = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Directory'), startingDir, QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)

		return dialog


	def colorPickerDialog(self, current_color=None):
		""" Opens a system dialog for choosing a colour.
			Return the selected colour as a QColor object, or None if the
			dialog is cancelled.
		"""
		color_dialog = QtWidgets.QColorDialog()
		#color_dialog.setOption(QtWidgets.QColorDialog.DontUseNativeDialog)

		# Set current colour
		if current_color is not None:
			color_dialog.setCurrentColor(current_color)

		# Only return a color if valid / dialog accepted
		if color_dialog.exec_() == color_dialog.Accepted:
			color = color_dialog.selectedColor()
			return color


	# ------------------------------------------------------------------------
	# Widget handlers

	def setupWidgets(self, 
		             parentObject, 
		             forceCategory=None, 
		             inherit=None, 
		             storeProperties=True, 
		             updateOnly=False):
		""" Set up all the child widgets of the specified parent object.

			If 'forceCategory' is specified, this will override the category
			of all child widgets.
			'inherit' specifies an alternative XML data source for widgets
			to get their values from.
			If 'storeProperties' is True, the values will be stored in the XML
			data as well as applied to the widgets.
			If 'updateOnly' is True, only the widgets' values will be updated.
		"""
		if forceCategory is not None:
			category = forceCategory

		if updateOnly:
			storeProperties = False

		for widget in parentObject.findChildren(QtWidgets.QWidget):

			# Enable expansion of custom rollout group box controls...
			if widget.property('expandable'):
				if isinstance(widget, QtWidgets.QGroupBox):
					widget.setCheckable(True)
					# widget.setChecked(expand)
					widget.setFixedHeight(widget.sizeHint().height())
					if not updateOnly:
						widget.toggled.connect(self.toggleExpandGroup)

			# Set up handler for push buttons...
			if widget.property('exec'):
				if isinstance(widget, QtWidgets.QPushButton):
					if not updateOnly:
						widget.clicked.connect(self.execPushButton)

			# Set up handlers for different widget types & apply values
			attr = widget.property('xmlTag')
			if attr:
				self.base_widget = widget.objectName()
				if forceCategory is None:
					category = self.findCategory(widget)
				if category:
					widget.setProperty('xmlCategory', category)

					if inherit is None:
						pass
						#value = self.xd.getValue(category, attr)
						value = ""
					else:
						#value = self.xd.getValue(category, attr)
						value = ""
						if value == "":
							value = inherit.getValue(category, attr)

							# widget.setProperty('xmlTag', None)
							widget.setProperty('inheritedValue', True)
							widget.setToolTip("This value is being inherited. Change the value to override the inherited value.")  # Rework this in case widgets already have a tooltip

							# Apply pop-up menu to remove override - can't get to work here
							# self.addContextMenu(widget, "Remove override", self.removeOverrides)
							# widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

							# actionRemoveOverride = QtWidgets.QAction("Remove override", None)
							# actionRemoveOverride.triggered.connect(self.removeOverrides)
							# widget.addAction(actionRemoveOverride)


					# Spin boxes...
					if isinstance(widget, QtWidgets.QSpinBox):
						if value is not "":
							widget.setValue(int(value))
						if storeProperties:
							self.storeValue(category, attr, widget.value())
						if not updateOnly:
							widget.valueChanged.connect(self.storeSpinBoxValue)

					# Double spin boxes...
					elif isinstance(widget, QtWidgets.QDoubleSpinBox):
						if value is not "":
							widget.setValue(float(value))
						if storeProperties:
							self.storeValue(category, attr, widget.value())
						if not updateOnly:
							widget.valueChanged.connect(self.storeSpinBoxValue)

					# Line edits...
					elif isinstance(widget, QtWidgets.QLineEdit):
						if value is not "":
							widget.setText(value)
						if storeProperties:
							self.storeValue(category, attr, widget.text())
						if not updateOnly:
							# widget.textEdited.connect(self.storeLineEditValue)
							widget.textChanged.connect(self.storeLineEditValue)

					# Plain text edits...
					elif isinstance(widget, QtWidgets.QPlainTextEdit):
						if value is not "":
							widget.setPlainText(value)
						if storeProperties:
							self.storeValue(category, attr, widget.toPlainText())
						if not updateOnly:
							widget.textChanged.connect(self.storeTextEditValue)

					# Check boxes...
					elif isinstance(widget, QtWidgets.QCheckBox):
						if value is not "":
							if value == "True":
								widget.setCheckState(QtCore.Qt.Checked)
							elif value == "False":
								widget.setCheckState(QtCore.Qt.Unchecked)
						if storeProperties:
							self.storeValue(category, attr, self.getCheckBoxValue(widget))
						if not updateOnly:
							widget.toggled.connect(self.storeCheckBoxValue)

					# Radio buttons...
					elif isinstance(widget, QtWidgets.QRadioButton):
						if value is not "":
							widget.setAutoExclusive(False)
							if value == widget.text():
								widget.setChecked(True)
							else:
								widget.setChecked(False)
							widget.setAutoExclusive(True)
						if storeProperties:
							if widget.isChecked():
								self.storeValue(category, attr, widget.text())
						if not updateOnly:
							widget.toggled.connect(self.storeRadioButtonValue)

					# Combo boxes...
					elif isinstance(widget, QtWidgets.QComboBox):
						if value is not "":
							if widget.findText(value) == -1:
								widget.addItem(value)
							widget.setCurrentIndex(widget.findText(value))
						if storeProperties:
							self.storeValue(category, attr, widget.currentText())
						if not updateOnly:
							if widget.isEditable():
								widget.editTextChanged.connect(self.storeComboBoxValue)
							else:
								widget.currentIndexChanged.connect(self.storeComboBoxValue)


	def findCategory(self, widget):
		""" Recursively check the parents of the given widget until a custom
			property 'xmlCategory' is found.
		"""
		if widget.property('xmlCategory'):
			print("Category '%s' found for '%s'." %(widget.property('xmlCategory'), widget.objectName()))
			return widget.property('xmlCategory')
		else:
			# Stop iterating if the widget's parent in the main window...
			if isinstance(widget.parent(), QtWidgets.QMainWindow):
				print("No category could be found for '%s'. The widget's value cannot be stored." %self.base_widget)
				return None
			else:
				return self.findCategory(widget.parent())


	def addContextMenu(self, widget, name, command, icon=None):
		""" Add context menu item to widget.

			'widget' should be a Push Button or Tool Button.
			'name' is the text to be displayed in the menu.
			'command' is the function to run when the item is triggered.
			'icon' is a pixmap to use for the item's icon (optional).
		"""
		widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		actionName = "action%s" %re.sub(r"[^\w]", "_", name)

		action = QtWidgets.QAction(name, None)
		if icon:
			actionIcon = QtGui.QIcon()
			#actionIcon.addPixmap(QtGui.QPixmap(osOps.absolutePath("$IC_FORMSDIR/rsc/%s.png" %icon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			#actionIcon.addPixmap(QtGui.QPixmap(osOps.absolutePath("$IC_FORMSDIR/rsc/%s_disabled.png" %icon)), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
			action.setIcon(actionIcon)
		action.setObjectName(actionName)
		action.triggered.connect(command)
		widget.addAction(action)

		# Make a class-scope reference to this object
		# (won't work without it for some reason)
		exec_str = "self.%s = action" %actionName
		exec(exec_str)


	def toggleExpertWidgets(self, isExpertMode, parentObject):
		""" Show/hide all widgets with the custom property 'expert' under
			the specified parentObject.
		"""
		types = (
			QtWidgets.QMenu, 
			QtWidgets.QMenuBar, 
			QtWidgets.QAction, 
			)

		try:
			for item in parentObject.findChildren(types):
				if item.property('expert'):
					item.setVisible(isExpertMode)

		# Fix for Qt4 where findChildren signature doesn't suport a tuple for
		# an argument...
		except TypeError:
			expert_items = []
			for widget_type in types:
				for item in parentObject.findChildren(widget_type):
					if item.property('expert'):
						expert_items.append(item)
			for item in expert_items:
				item.setVisible(isExpertMode)


	def conformFormLayoutLabels(self, parentObject, padding=8):
		""" Conform the widths of all labels in formLayouts under the
			specified parentObject for a more coherent appearance.

			'padding' is an amount in pixels to add to the max width.
		"""
		labels = []
		labelWidths = []

		# Find all labels
		for layout in parentObject.findChildren(QtWidgets.QFormLayout):
			# print(layout.objectName())
			items = (layout.itemAt(i) for i in range(layout.count()))
			for item in items:
				widget = item.widget()
				if isinstance(widget, QtWidgets.QLabel):
					labels.append(widget)

		# Find label widths
		for label in labels:
			fontMetrics = QtGui.QFontMetrics(label.font())
			width = fontMetrics.width(label.text())
			#print('Width of "%s": %d px' %(label.text(), width))
			labelWidths.append(width)

		# Get widest label & set all labels widths to match
		if labelWidths:
			maxWidth = max(labelWidths)
			#print("Max label width : %d px (%d inc padding)" %(maxWidth, maxWidth+padding))
			for label in labels:
				label.setFixedWidth(maxWidth+padding)
				label.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)


	def getCheckBoxValue(self, checkBox):
		""" Get the value from a checkbox and return a Boolean value.
		"""
		if checkBox.checkState() == QtCore.Qt.Checked:
			return True
		else:
			return False


	def getWidgetMeta(self, widget):
		""" 
		"""
		widget.setProperty('inheritedValue', False)
		widget.setToolTip("")  # Rework this in case widgets already have a tooltip
		widget.style().unpolish(widget)
		widget.style().polish(widget)

		category = widget.property('xmlCategory')
		attr = widget.property('xmlTag')
		return category, attr


	# @QtCore.Slot()
	def execPushButton(self):
		""" Execute the function associated with a button.
			***NOT YET IMPLEMENTED***
		"""
		print("%s %s" %(self.sender().objectName(), self.sender().property('exec')))


	# @QtCore.Slot()
	def storeSpinBoxValue(self):
		""" Get the value from a Spin Box and store in XML data.
		"""
		# category = self.sender().property('xmlCategory')
		# attr = self.sender().property('xmlTag')
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().value()
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeLineEditValue(self):
		""" Get the value from a Line Edit and store in XML data.
		"""
		# category = self.sender().property('xmlCategory')
		# attr = self.sender().property('xmlTag')
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().text()
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeTextEditValue(self):
		""" Get the value from a Plain Text Edit and store in XML data.
		"""
		# category = self.sender().property('xmlCategory')
		# attr = self.sender().property('xmlTag')
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().toPlainText()
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeCheckBoxValue(self):
		""" Get the value from a Check Box and store in XML data.
		"""
		# category = self.sender().property('xmlCategory')
		# attr = self.sender().property('xmlTag')
		category, attr = self.getWidgetMeta(self.sender())
		value = self.getCheckBoxValue(self.sender())
		self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeRadioButtonValue(self):
		""" Get the value from a Radio Button group and store in XML data.
		"""
		if self.sender().isChecked():
			# category = self.sender().property('xmlCategory')
			# attr = self.sender().property('xmlTag')
			category, attr = self.getWidgetMeta(self.sender())
			value = self.sender().text()
			self.storeValue(category, attr, value)


	# @QtCore.Slot()
	def storeComboBoxValue(self):
		""" Get the value from a Combo Box and store in XML data.
		"""
		# category = self.sender().property('xmlCategory')
		# attr = self.sender().property('xmlTag')
		category, attr = self.getWidgetMeta(self.sender())
		value = self.sender().currentText()
		self.storeValue(category, attr, value)


	def storeValue(self, category, attr, value=""):
		""" Store value in XML data.
		"""
		currentAttrStr = "%20s %s.%s" %(type(value), category, attr)
		# if currentAttrStr == self.currentAttrStr:
		# 	print("%s=%s" %(currentAttrStr, value), inline=True)
		# else:
		# 	print("%s=%s" %(currentAttrStr, value))
		print("%s=%s" %(currentAttrStr, value))
		# userPrefs.edit(category, attr, value)
		#self.xd.setValue(category, attr, str(value))
		self.currentAttrStr = currentAttrStr


	# @QtCore.Slot()
	def toggleExpandGroup(self):
		""" Toggle expansion of custom rollout group box control.
		"""
		groupBox = self.sender()
		state = groupBox.isChecked()
		if state:
			groupBox.setFixedHeight(groupBox.sizeHint().height())
		else:
			groupBox.setFixedHeight(20)  # Slightly hacky - needs to match value defined in QSS

		#self.setFixedHeight(self.sizeHint().height())  # Resize window


	def populateComboBox(self, comboBox, contents, replace=True, addEmptyItems=False):
		""" Use a list (contents) to populate a combo box.
			If 'replace' is true, the existing items will be replaced,
			otherwise the contents will be appended to the existing items.
		"""
		# Store current value
		current = comboBox.currentText()

		# Clear menu
		if replace:
			comboBox.clear()

		# Populate menu
		if contents:
			for item in contents:
				if addEmptyItems:
					comboBox.addItem(item)
				else:
					if item:
						comboBox.addItem(item)

		# Set to current value
		index = comboBox.findText(current)
		if index == -1:
			comboBox.setCurrentIndex(0)
		else:
			comboBox.setCurrentIndex(index)

	# End widget handlers
	# ------------------------------------------------------------------------


	# def loadUIFile(self):
	# 	""" Load/reload UI file.
	# 	"""
	# 	self.ui = QtCompat.loadUi(UI_FILE, self)


	def loadStyleSheet(self):
		""" Load/reload stylesheet.
		"""
		if self.stylesheet:
			#import style_vars

			with open(self.stylesheet, 'r') as fh:
				stylesheet = fh.read()

				# if accent_color:
				# 	rgb = "%d, %d, %d" %(accent_color.red(), accent_color.green(), accent_color.blue())
				# 	stylesheet = fh.read().replace("112, 158, 50", rgb)  # "0, 120, 215"
				# else:
				# 	stylesheet = fh.read()

			#for key, value in style_vars.var.items():
			for key, value in self.col.items():
				rgb = "%d, %d, %d" %(value.red(), value.green(), value.blue())
				stylesheet = stylesheet.replace("%"+key+"%", rgb)

			self.ui.setStyleSheet(stylesheet)


	# def reloadStyleSheet(self):
	# 	""" Reload stylesheet.
	# 	"""
	# 	if self.stylesheet:
	# 		#qss = os.path.join(os.environ['IC_FORMSDIR'], self.stylesheet)
	# 		qss = self.stylesheet
	# 		with open(qss, "r") as fh:
	# 			self.setStyleSheet(fh.read()) #.replace("112, 158, 50", "0, 120, 215"))


	# def contrast(self, color1, color2, min_contrast=68, lighter=False, darker=False):
	# 	""" Find the brightness variation between two colours and return a
	# 		color that has good contrast with color2 (at least the value of
	# 		min_contrast).
	# 	"""
	# 	contrast = abs(color1.lightness()-color2.lightness())
	# 	if contrast < min_contrast:
	# 		print "low contrast warning: %d" %contrast

	# 		if lighter:
	# 			color3 = QtGui.QColor(color2.red()+min_contrast, color2.green()+min_contrast, color2.blue()+min_contrast)
	# 			#print color3.name()
	# 			return color3
	# 		elif darker:
	# 			color3 = QtGui.QColor(color2.red()-min_contrast, color2.green()-min_contrast, color2.blue()-min_contrast)
	# 			#print color3.name()
	# 			return color3
	# 	else:  # Color has sufficient contrast
	# 		return color1


	def offsetColor(self, input_color, amount, clamp=None):
		""" .
		"""
		if amount == 0:
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
		return QtGui.QColor(lum, lum, lum)


	def computeUIPalette(self):
		""" Compute UI colours based on window colour.
		"""
		self.col['text'] = QtGui.QColor(204, 204, 204)
		self.col['disabled'] = QtGui.QColor(102, 102, 102)
		self.col['base'] = QtGui.QColor(34, 34, 34)
		self.col['button'] = QtGui.QColor(102, 102, 102)
		self.col['hover'] = QtGui.QColor(119, 119, 119)
		#self.col['pressed'] = QtGui.QColor(60, 60, 60)
		self.col['pressed'] = self.col['highlight']
		self.col['checked'] = QtGui.QColor(51, 51, 51)
		self.col['menu-bg'] = QtGui.QColor(51, 51, 51)
		self.col['menu-border'] = QtGui.QColor(68, 68, 68)
		self.col['group-bg'] = QtGui.QColor(128, 128, 128)
		self.col['line'] = self.col['window'].darker(110)
		self.col['highlighted-text'] = QtGui.QColor(255, 255, 255)

		if self.col['window'].lightness() < 128:  # Dark UI
			self.col['text'] = self.offsetColor(self.col['window'], +68, 204)
			self.col['base'] = self.offsetColor(self.col['window'], -34, 34)
			self.col['alternate'] = self.offsetColor(self.col['base'], +8)
			self.col['button'] = self.offsetColor(self.col['window'], +34, 102)
			self.col['menu-bg'] = self.offsetColor(self.col['window'], -17, 68)
			self.col['menu-border'] = self.offsetColor(self.col['menu-bg'], +17)
			#self.col['group-bg'] = QtGui.QColor(127, 127, 127)
		else:  # Light UI
			self.col['text'] = self.offsetColor(self.col['window'], -68, 51)
			self.col['base'] = self.offsetColor(self.col['window'], +34, 221)
			self.col['alternate'] = self.offsetColor(self.col['base'], -8)
			self.col['button'] = self.offsetColor(self.col['window'], -34, 187)
			self.col['menu-bg'] = self.offsetColor(self.col['window'], +17, 187)
			self.col['menu-border'] = self.offsetColor(self.col['menu-bg'], -17)
			#self.col['group-bg'] = QtGui.QColor(128, 128, 128)

		self.col['hover'] = self.offsetColor(self.col['button'], +17)
		self.col['checked'] = self.offsetColor(self.col['button'], -17)
		#print("hover: %s" %self.col['hover'].name())

		if self.col['highlight'].lightness() < 192:
			self.col['highlighted-text'] = QtGui.QColor(255, 255, 255)
			#self.col['highlighted-text'] = self.contrast(QtGui.QColor(255, 255, 255), self.col['highlight'], 68)
		else:
			self.col['highlighted-text'] = QtGui.QColor(0, 0, 0)
			#self.col['highlighted-text'] = self.contrast(QtGui.QColor(0, 0, 0), self.col['highlight'], 68)

		if self.col['button'].lightness() < 192:
			#self.col['button-text'] = QtGui.QColor(255, 255, 255)
			self.col['button-text'] = self.offsetColor(self.col['button'], +68, 204)
		else:
			#self.col['button-text'] = QtGui.QColor(0, 0, 0)
			self.col['button-text'] = self.offsetColor(self.col['button'], -68, 51)


	# @QtCore.Slot()
	def setUIBrightness(self, value):
		""" Set the UI style background shade.
		"""
		print(value)
		self.col['window'] = QtGui.QColor(value, value, value)
		self.computeUIPalette()
		self.loadStyleSheet()


	# @QtCore.Slot()
	def setAccentColor(self, color=None):
		""" Set the UI style accent colour.
		"""
		widget = self.sender()

		# Get current colour and pass to function
		current_color = widget.palette().color(QtGui.QPalette.Background)
		color = self.colorPickerDialog(current_color)
		if color:
			widget.setStyleSheet("QWidget { background-color: %s }" %color.name())
			self.col['highlight'] = color
			self.computeUIPalette()
			self.loadStyleSheet()


	def storeWindow(self):
		""" Store window geometry and state.
			(Save state may cause issues with PyQt5)
		"""
		if self.store_window_geometry:
			#if os.environ['IC_ENV'] == 'STANDALONE':
			print("Storing window geometry for '%s'." %self.objectName())
			try:
				self.settings.setValue("geometry", self.saveGeometry())
				# self.settings.setValue("windowState", self.saveState())
			except:
				pass


	# def showEvent(self, event):
	# 	""" Event handler for when window is shown.
	# 	"""
	# 	pass


	# def closeEvent(self, event):
	# 	""" Event handler for when window is closed.
	# 	"""
	# 	self.storeWindow()
	# 	QtWidgets.QMainWindow.closeEvent(self, event)
	# 	#self.closeEvent(self, event)


	def save(self):
		""" Save data.
		"""
		# if self.xd.saveXML():
		# 	return True
		# else:
		# 	return False
		return True


	# def saveAndExit(self):
	# 	""" Save data and close window.
	# 	"""
	# 	if self.save():
	# 		self.returnValue = True
	# 		self.hide()
	# 		self.ui.hide()
	# 		#self.exit()
	# 	else:
	# 		self.exit()


	# def exit(self):
	# 	""" Exit the window with negative return value.
	# 	"""
	# 	self.storeWindow()
	# 	#self.returnValue = False
	# 	self.hide()

# ----------------------------------------------------------------------------
# End of main window class
# ============================================================================
# DCC application helper functions
# ----------------------------------------------------------------------------

def _maya_delete_ui(window_object, window_title):
	""" Delete existing UI in Maya.
	"""
	if mc.window(window_object, query=True, exists=True):
		mc.deleteUI(window_object)  # Delete window
	if mc.dockControl('MayaWindow|' + window_title, query=True, exists=True):
		mc.deleteUI('MayaWindow|' + window_title)  # Delete docked window


# def _houdini_delete_ui(window_object, window_title):
# 	""" Delete existing UI in Houdini.
# 	"""
# 	pass


def _nuke_delete_ui(window_object, window_title):
	""" Delete existing UI in Nuke.
	"""
	for obj in QtWidgets.QApplication.allWidgets():
		if obj.objectName() == window_object:
			obj.deleteLater()


def _maya_main_window():
	""" Return Maya's main window.
	"""
	for obj in QtWidgets.QApplication.topLevelWidgets():
		if obj.objectName() == 'MayaWindow':
			return obj
	raise RuntimeError("Could not find MayaWindow instance")


# def _houdini_main_window():
# 	""" Return Houdini's main window.
# 	"""
# 	return hou.qt.mainWindow()
# 	raise RuntimeError("Could not find Houdini's main window instance")


def _nuke_main_window():
	""" Returns Nuke's main window.
	"""
	for obj in QtWidgets.QApplication.topLevelWidgets():
		if (obj.inherits('QMainWindow') and obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
			return obj
	raise RuntimeError("Could not find DockMainWindow instance")


def _nuke_set_zero_margins(widget_object):
	""" Remove Nuke margins when docked UI.
		More info:
		https://gist.github.com/maty974/4739917
	"""
	parentApp = QtWidgets.QApplication.allWidgets()
	parentWidgetList = []
	for parent in parentApp:
		for child in parent.children():
			if widget_object.__class__.__name__ == child.__class__.__name__:
				parentWidgetList.append(parent.parentWidget())
				parentWidgetList.append(parent.parentWidget().parentWidget())
				parentWidgetList.append(parent.parentWidget().parentWidget().parentWidget())

				for sub in parentWidgetList:
					for tinychild in sub.children():
						try:
							tinychild.setContentsMargins(0, 0, 0, 0)
						except:
							pass



class IconProvider(QtWidgets.QFileIconProvider):
	def icon(self, fileInfo):
		if fileInfo.isDir():
			return QtGui.QIcon(':/rsc/rsc/icon_folder.png') 
		return QtWidgets.QFileIconProvider.icon(self, fileInfo)


# ----------------------------------------------------------------------------
# Run functions
# ----------------------------------------------------------------------------

# def run_(**kwargs):
# 	# for key, value in kwargs.iteritems():
# 	# 	print "%s = %s" % (key, value)
# 	customUI = TemplateUI(**kwargs)
# 	#customUI.setAttribute( QtCore.Qt.WA_DeleteOnClose )
# 	print customUI
# 	customUI.show()
# 	#customUI.raise_()
# 	#customUI.exec_()


# def run_maya(**kwargs):
# 	""" Run in Maya.
# 	"""
# 	_maya_delete_ui()  # Delete any already existing UI
# 	customUI = TemplateUI(parent=_maya_main_window())

# 	# Makes Maya perform magic which makes the window stay on top in OS X and
# 	# Linux. As an added bonus, it'll make Maya remember the window position.
# 	customUI.setProperty("saveWindowPref", True)

# 	customUI.display(**kwargs)  # Show the UI


# def run_nuke(**kwargs):
# 	""" Run in Nuke.
# 	"""
# 	_nuke_delete_ui()  # Delete any already existing UI
# 	customUI = TemplateUI(parent=_nuke_main_window())

# 	customUI.display(**kwargs)  # Show the UI


# # Detect environment and run application
# if os.environ['IC_ENV'] == 'STANDALONE':
# 	pass
# elif os.environ['IC_ENV'] == 'MAYA':
# 	import maya.cmds as mc
# 	# run_maya()
# elif os.environ['IC_ENV'] == 'NUKE':
# 	import nuke
# 	import nukescripts
# 	# run_nuke()
# # elif __name__ == '__main__':
# # 	run_standalone()

