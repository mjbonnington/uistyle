from Qt import QtGui, QtWidgets


class UnsavedFileDialog(QtWidgets.QMessageBox):
    """Display a message box dialog to ask whether to save a file that's been 
    modified.
    """
    def __init__(self, parent=None):
        super(UnsavedFileDialog, self).__init__(parent)


    def display(self, doctype="file"):
        """Show the dialog.

        Keyword arguments:
            doctype (str) - override the terminology for a file, e.g. 'scene'
            in Maya or 'script' in Nuke.
        """
        self.setWindowTitle("Unsaved {}".format(doctype.capitalize()))
        self.setText("The current {} has been modified.".format(doctype.lower()))
        self.setInformativeText("Do you want to save your changes?")
        self.setStandardButtons(self.Save | self.Discard | self.Cancel)
        self.setDefaultButton(self.Save)

        # Remove default button icons
        self.button(self.Save).setIcon(QtGui.QIcon())
        self.button(self.Discard).setIcon(QtGui.QIcon())
        self.button(self.Cancel).setIcon(QtGui.QIcon())

        # Override button text
        self.button(self.Discard).setText("Discard")

        result = self.exec_()

        if result == self.Save:
            self.accept()
            return "Yes"
        elif result == self.Discard:
            self.close()
            return "No"
        elif result == self.Cancel:
            self.reject()
            return "Cancel"
