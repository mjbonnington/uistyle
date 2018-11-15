#!/usr/bin/python

# style__main__.py
# Template for Qt GUI application written in Python
# Uses Qt.py for compatibility with all Python bindings.
#
# Directions for use:
# 
# Create your UI in Qt Designer and save as (e.g) 'style.ui'
# No need to compile your UI with pyside-uic as we load the .ui file directly.
# 
# Save your resources file as (e.g.) 'style.qrc'
# Compile resources to with command: 'pyside-rcc style.qrc -o style_rc.py'
# For compatibility with PySide2, replace 'from [PySide/PyQt] import QtCore'
# with 'from Qt import QtCore'
# 
# Run with command: 'python ./style__main__.py'


import sys

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Set the UI and the stylesheet
UI_FILE = "style_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet


class UITestApp(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Main application class.
	"""
	def __init__(self, parent=None):
		super(UITestApp, self).__init__(parent)
		self.parent = parent

		self.setupUI(window_object='styleUI', 
					 ui_file=UI_FILE, 
					 stylesheet=STYLESHEET, 
					 store_window_geometry=True)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Window)

		# Restore widget state
		try:
			self.ui.splitter.restoreState(self.settings.value("splitterSizes")) #.toByteArray())
			#self.ui.renderQueue_treeWidget.header().restoreState(self.settings.value("renderQueueView")) #.toByteArray())
		except:
			pass

		# Load UI
		#self.loadUIFile()
		self.show()

		self.info()

		# Connect signals & slots
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.exit)
		#self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.loadStyleSheet)

		self.ui.colorChooser_button.setStyleSheet("QWidget { background-color: %s }" %self.col['highlight'].name())
		self.ui.colorChooser_button.clicked.connect(self.setAccentColor)
		self.ui.uiBrightness_slider.setValue(self.col['window'].lightness())
		self.ui.uiBrightness_slider.valueChanged.connect(self.setUIBrightness)
		#self.ui.reloadUI_pushButton.clicked.connect(self.loadUIFile)
		self.ui.reloadStylesheet_pushButton.clicked.connect(self.loadStyleSheet)

		# Add 'Sort by' separator label
		label = QtWidgets.QLabel("Sort by:")
		sortBy_separator = QtWidgets.QWidgetAction(self)
		sortBy_separator.setDefaultWidget(label)
		self.ui.menuEdit.insertAction(self.ui.actionName, sortBy_separator)

		# Make 'Sort by' actions mutually exclusive
		alignmentGroup = QtWidgets.QActionGroup(self)
		alignmentGroup.addAction(self.ui.actionName)
		alignmentGroup.addAction(self.ui.actionSize)
		alignmentGroup.addAction(self.ui.actionType)
		alignmentGroup.addAction(self.ui.actionDate)

		# Add 'Other' separator label
		label = QtWidgets.QLabel("Other:")
		other_separator = QtWidgets.QWidgetAction(self)
		other_separator.setDefaultWidget(label)
		other_separator.setEnabled(False)
		self.ui.menuEdit.insertAction(self.ui.actionAttribute, other_separator)

		# Make 'Other' actions mutually exclusive
		otherGroup = QtWidgets.QActionGroup(self)
		otherGroup.addAction(self.ui.actionAttribute)
		otherGroup.addAction(self.ui.actionObject)


	# [Application code goes here]


	def info(self):
		""" Return some version info about Python, Qt, binding, etc.
		"""
		from Qt import __binding__, __binding_version__

		print("Python %d.%d.%d" %(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
		print("%s %s" %(__binding__, __binding_version__))
		print("Qt %s" %QtCore.qVersion())


	def exit(self):
		""" Exit the UI.
		"""
		print("Exit the UI.")
		self.ui.hide()
		if __name__ == "__main__":
			sys.exit()


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		# Store window geometry and state of certain widgets
		self.storeWindow()
		self.settings.setValue("splitterSizes", self.ui.splitter.saveState())
		#self.settings.setValue("renderQueueView", self.ui.renderQueue_treeWidget.header().saveState())

		QtWidgets.QMainWindow.closeEvent(self, event)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	# Apply application style.
	# app.setStyle('Fusion')  # Qt5

	# Hack to fix 'etching' on disabled text
	pal = QtWidgets.QApplication.palette()
	#pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(102, 102, 102))
	pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(0, 0, 0, 0))
	app.setPalette(pal);

	myApp = UITestApp()
	sys.exit(app.exec_())

else:
	myApp = UITestApp()


