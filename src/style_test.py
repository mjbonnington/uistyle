#!/usr/bin/python

# style_test.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2018-2022
#
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
# Run with command: 'python ./style_test.py'

import os
import sys

from Qt import QtCompat, QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
import imagebutton


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

prefs_location = os.getenv('IC_USERPREFSDIR', os.path.expanduser('~/.uistyle'))
if not os.path.isdir(prefs_location):
	os.makedirs(prefs_location)

cfg = dict(
	app_id="ic_ui",  # This should match the Rez package name
	app_name="Style Test",

	description="Template for Qt GUI application written in Python.\nUses Qt.py for compatibility with all Python bindings.",
	credits="Principal developer: Mike Bonnington",

	ui_file=os.path.join(os.path.dirname(__file__), "forms", "style_test.ui"),
	stylesheet="style.qss",
	icon="color.svg",

	prefs_file=os.path.join(prefs_location, 'appearance_prefs.json'), 
	store_window_geometry=True, 
)


# ----------------------------------------------------------------------------
# Begin main application class
# ----------------------------------------------------------------------------

class StyleTestApp(QtWidgets.QMainWindow, UI.TemplateUI):
	"""Main application class."""

	def __init__(self, parent=None):
		super(StyleTestApp, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)

		# Set window flags and other Qt attributes
		self.setWindowFlags(QtCore.Qt.Window)

		# Connect signals & slots --------------------------------------------

		self.ui.actionOpen_UI.triggered.connect(self.openUI)
		self.ui.actionOpen_Stylesheet.triggered.connect(self.open_qss)
		self.ui.actionSave_Stylesheet.triggered.connect(self.save_qss)
		self.ui.actionAbout.triggered.connect(self.about_dialog)
		self.ui.actionDynamic_QSS.triggered.connect(self.set_dynamic_style)
		self.ui.actionQuit.triggered.connect(self.exit)

		# self.ui.base_colorChooser_button.setStyleSheet("QWidget { background-color: %s }" % self.col['window'].name())
		# # self.ui.base_colorChooser_button.colorChanged.connect(lambda: self.appearance.set_ui_color('window'))
		# self.ui.accent_colorChooser_button.setStyleSheet("QWidget { background-color: %s }" % self.col['highlight'].name())
		# # self.ui.accent_colorChooser_button.colorChanged.connect(lambda: self.appearance.set_ui_color('highlight'))
		# self.ui.uiBrightness_slider.setValue(self.col['window'].lightness())
		self.ui.uiBrightness_slider.valueChanged.connect(lambda value: self.appearance.set_ui_brightness(value))
		self.ui.fontSize_spinBox.valueChanged.connect(lambda value: self.appearance.set_font_size(value))
		self.ui.resetStylesheet_pushButton.clicked.connect(self.reset_appearance)
		self.colorChanged.connect(lambda attr, color: self.appearance.set_ui_color(attr, color))
		self.colorChanged.connect(lambda: self.ui.uiBrightness_slider.setValue(self.col['window'].lightness()))

		self.ui.loadedUIs_tabWidget.tabCloseRequested.connect(lambda index: self.ui.loadedUIs_tabWidget.removeTab(index))  # Allow tabs to be closed

		# Add popup menus to buttons -----------------------------------------

		self.ui.menu1_pushButton.setMenu(self.ui.menuTest)
		self.ui.popup1_toolButton.setMenu(self.ui.menuTest)
		self.ui.popup2_toolButton.setMenu(self.ui.menuAnother)
		self.ui.popup3_toolButton.setMenu(self.ui.menuAnother)
		self.ui.popup4_toolButton.setMenu(self.ui.menuTest)
		self.ui.menuButtonPopup_toolButton.setMenu(self.ui.menuTest)
		self.ui.menuButtonPopupWithIcon_toolButton.setMenu(self.ui.menuAnother)
		self.ui.menuButtonPopupWithIconBeside_toolButton.setMenu(self.ui.menuAnother)

		# Set up image thumbnail browser button ------------------------------

		self.ui.thumbnail_imageButton = imagebutton.ImageButton(max_size=[512, 288])
		# self.ui.thumbnail_verticalLayout.insertWidget(0, self.ui.thumbnail_imageButton)
		self.ui.thumbnail_verticalLayout.addWidget(self.ui.thumbnail_imageButton)
		self.ui.thumbnail_lineEdit.hide()

		# self.ui.thumbnail_imageButton.clicked.connect(lambda: self.browse_file(self.ui.thumbnail_lineEdit, 'Image files (*.jpg *.png *.gif)'))
		self.ui.thumbnail_imageButton.imageChanged.connect(lambda imgpath: self.ui.thumbnail_lineEdit.setText(imgpath))
		self.ui.thumbnail_lineEdit.textChanged.connect(lambda text: self.ui.thumbnail_imageButton.updateThumbnail(text))

		# Setup menus --------------------------------------------------------

		# Add 'Sort by' separator label
		label = QtWidgets.QLabel("Sort by:")
		sortBy_separator = QtWidgets.QWidgetAction(self)
		sortBy_separator.setDefaultWidget(label)
		self.ui.menuAnother.insertAction(self.ui.actionName, sortBy_separator)

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
		self.ui.menuAnother.insertAction(self.ui.actionAttribute, other_separator)

		# Make 'Other' actions mutually exclusive
		otherGroup = QtWidgets.QActionGroup(self)
		otherGroup.addAction(self.ui.actionAttribute)
		otherGroup.addAction(self.ui.actionObject)

		# --------------------------------------------------------------------

		self.reset_appearance()
		self.build_styles()
		self.show()


	# [Application code goes here] -------------------------------------------


	def set_icons(self):
		self.ui.info_toolButton.setIcon(self.iconSet('help-about.svg'))
		self.ui.mixed_toolButton.setIcon(self.iconSet('applications-utilities-symbolic.svg'))
		self.ui.test1_toolButton.setIcon(self.iconSet('computer-symbolic.svg'))
		self.ui.test2_toolButton.setIcon(self.iconSet(['folder.svg', 'folder-open.svg']))
		self.ui.popup1_toolButton.setIcon(self.iconSet('utilities-terminal-symbolic.svg'))
		self.ui.popup2_toolButton.setIcon(self.iconSet('web-browser-symbolic.svg'))
		self.ui.test3_toolButton.setIcon(self.iconSet('add.svg'))
		self.ui.test4_toolButton.setIcon(self.iconSet(['object-locked.svg', 'object-unlocked.svg']))
		self.ui.popup3_toolButton.setIcon(self.iconSet('edit.svg'))
		self.ui.popup4_toolButton.setIcon(self.iconSet('clear.svg'))
		self.ui.menuButtonPopupWithIcon_toolButton.setIcon(self.iconSet('system-file-manager-symbolic.svg'))
		self.ui.menuButtonPopupWithIconBeside_toolButton.setIcon(self.iconSet(['layer-visible-off.svg', 'layer-visible-on.svg']))


	def reset_appearance(self):
		self.ui.base_colorChooser_button.setStyleSheet("QWidget { background-color: %s }" % self.col['sys-window'].name())
		self.ui.accent_colorChooser_button.setStyleSheet("QWidget { background-color: %s }" % self.col['sys-highlight'].name())
		self.ui.uiBrightness_slider.setValue(self.col['sys-window'].lightness())
		self.appearance.reset_()
		self.set_icons()
		self.ui.info_toolButton.setToolTip("window-color: {}\naccent-color: {}".format(self.col['window'].name(), self.col['highlight'].name()))


	def build_styles(self):
		"""Create menus for predefined Qt styles."""

		alignmentGroup = QtWidgets.QActionGroup(self)
		alignmentGroup.addAction(self.ui.actionDynamic_QSS)
		for style in QtWidgets.QStyleFactory.keys():
			action_name = "action_style_%s" % style
			action = QtWidgets.QAction(style, None)
			action.setObjectName(action_name)
			action.setCheckable(True)
			action.setProperty("style", style)
			action.triggered.connect(self.set_style)
			self.ui.menuStyle.addAction(action)
			alignmentGroup.addAction(action)

			# Make a class-scope reference to this object
			# (won't work without it for some reason)
			exec_str = "self.%s = action" % action_name
			exec(exec_str)


	def set_style(self):
		"""Wrapper to apply predefined Qt style."""

		msg = self.appearance.set_qt_style(self.sender().property("style"))
		self.mixedControls_groupBox.hide()
		self.ui.statusbar.showMessage(msg)


	def set_dynamic_style(self):
		"""Wrapper to apply custom dynamic style."""

		self.appearance.read_stylesheet()
		self.mixedControls_groupBox.show()
		self.ui.statusbar.showMessage("Using custom dynamic stylesheet")


	def openUI(self):
		"""Load UI into its own tab."""

		ui_file = self.fileDialog(".", fileFilter="UI files (*.ui)")
		# Add and select new tab
		if ui_file:
			ui = QtCompat.loadUi(ui_file)
			tab_id = self.ui.loadedUIs_tabWidget.addTab(ui, os.path.basename(ui_file))
			self.ui.loadedUIs_tabWidget.setCurrentIndex(tab_id)
			self.setupWidgets(ui)
			self.conformFormLayoutLabels(ui)


	def open_qss(self):
		"""Load QSS stylesheet file and apply to UI."""

		qss_file = self.fileDialog(".", fileFilter="Qt Style Sheet files (*.qss)")
		# Load and set stylesheet
		if qss_file:
			self.appearance.qss = qss_file
			self.appearance.read_stylesheet()
			# self.setWindowTitle(cfg['window_title'] + " - " + os.path.basename(self.appearance.qss))


	def save_qss(self):
		"""Save QSS stylesheet."""

		qss_file = self.fileDialog(".", fileFilter="Qt Style Sheet files (*.qss)")
		if qss_file:
			self.appearance.write_stylesheet(qss_file)


	def exit(self):
		"""Exit the UI."""

		self.ui.hide()
		if __name__ == "__main__":
			sys.exit()


	# def closeEvent(self, event):
	# 	"""Event handler for when window is closed."""

	# 	# Store window geometry and state of certain widgets
	# 	self.save()  # Save settings
	# 	self.storeWindow()
	# 	self.settings.setValue("splitterSizes", self.ui.splitter.saveState())
	# 	# self.settings.setValue("renderQueueView", self.ui.renderQueue_treeWidget.header().saveState())

	# 	QtWidgets.QMainWindow.closeEvent(self, event)


	def hideEvent(self, event):
		"""Event handler for when window is hidden."""

		self.save()  # Save settings
		self.storeWindow()  # Store window geometry
		# self.storeWidgetState(self.ui.splitter, "splitterSizes")  # Store splitter size state
		# self.settings.setValue("taskView", self.ui.taskList_treeWidget.header().saveState())


# ----------------------------------------------------------------------------
# End main dialog class
# ============================================================================
# Run functions
# ----------------------------------------------------------------------------

def run(session):
	"""Run inside host app."""

	try:  # Show the UI
		session.styleTestUI.show()
	except AttributeError:  # Create the UI
		session.styleTestUI = StyleTestApp(parent=UI._main_window())
		session.styleTestUI.show()


if __name__ == "__main__":
	try:
		QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
	except AttributeError:
		pass
	app = QtWidgets.QApplication(sys.argv)

	# Hack to fix 'etching' on disabled text
	pal = QtWidgets.QApplication.palette()
	# pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(102, 102, 102))
	pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(0, 0, 0, 0))
	pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, QtGui.QColor(0, 0, 0, 0))
	pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, QtGui.QColor(0, 0, 0, 0))
	pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, QtGui.QColor(0, 0, 0, 0))
	pal.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, QtGui.QColor(0, 0, 0, 0))
	app.setPalette(pal)

	myApp = StyleTestApp()
	sys.exit(app.exec_())
