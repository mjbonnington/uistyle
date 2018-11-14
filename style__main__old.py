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

from Qt import QtCompat, QtCore, QtGui, QtWidgets
import rsc_rc  # Import resource file as generated by pyside-rcc / pyrcc5

# Set the UI and the stylesheet
UI_FILE = "style_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet


class TestApp(QtWidgets.QMainWindow):  # Replace 'TestApp' with the name of your app / Use 'QMainWindow' or 'QDialog' depending on the type of app
	""" Main application class.
	"""
	def __init__(self, parent=None):
		super(TestApp, self).__init__(parent)  # Replace 'TestApp' with the name of your app

		# Load UI
		self.loadUIFile()
		self.loadStyleSheet()
		self.show()

		self.info()

		# Connect signals & slots
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.exit)
		#self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.loadStyleSheet)

		self.ui.colorChooser_button.clicked.connect(self.colorPickerDialog)
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
		#print(type(self.ui))


	def loadUIFile(self):
		""" Load/reload UI file.
		"""
		self.ui = QtCompat.loadUi(UI_FILE, self)


	def loadStyleSheet(self, accent_color=None):
		""" Load/reload stylesheet.
		"""
		if STYLESHEET is not None:
			with open(STYLESHEET, "r") as fh:
				if accent_color:
					rgb = "%d, %d, %d" %(accent_color.red(), accent_color.green(), accent_color.blue())
					stylesheet = fh.read().replace("112, 158, 50", rgb)  # "0, 120, 215"
				else:
					stylesheet = fh.read()
				self.ui.setStyleSheet(stylesheet)


	def colorPickerDialog(self):
		""" Open a dialog to choose a color.
		"""
		color = QtWidgets.QColorDialog.getColor()
		if color:
			self.sender().setStyleSheet("QWidget { background-color: %s }" %color.name())
			self.loadStyleSheet(color)


	def exit(self):
		""" Exit the UI.
		"""
		print("Exit the UI.")
		self.ui.hide()
		if __name__ == "__main__":
			sys.exit()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	# Apply application style.
	# app.setStyle('Fusion')  # Qt5

	# Hack to fix 'etching' on disabled text
	pal = QtWidgets.QApplication.palette()
	#pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(102, 102, 102))
	pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(0, 0, 0, 0))
	app.setPalette(pal);

	myApp = TestApp()  # Replace 'TestApp' with the name of your app
	sys.exit(app.exec_())

else:
	myApp = TestApp()  # Replace 'TestApp' with the name of your app

