from Qt import QtCore, QtGui, QtWidgets


class MessageOverlay(QtWidgets.QWidget):
	"""Message overlay setup to be used by most of the GUI python tools."""

	def __init__(self, parent=None):
		"""Class constuctor."""

		super(MessageOverlay, self).__init__(parent)
		self.setup_ui()
		self.setVisible(False)
		self.setStyleSheet(
			"""
				QFrame#main_widget {
					background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #222, stop: 1 #111);
					border: 2px solid #333;
					border-radius: 6px;
					padding: 20px;
				}

				QLabel#label_title {
					font-weight: bold;
					font-size: 18px;
					color: #fff;
				}

				QLabel#horizontal_line {
					background: #555;
				}

				QLabel#label_message {
					font-size: 14px;
					color: #ccc;
				}
			"""
		)


	def setup_ui(self):
		"""Set up the Message Overlay widgets.

		+- main_widget (QFrame) -------------+
		|+- main_layout (QVBoxLayout)-------+|
		||                                  ||
		||       label_title (QLabel)       ||
		||                                  ||
		|| --- horizontal_line (QLabel) --- ||
		||                                  ||
		||      label_message (QLabel)      ||
		||                                  ||
		|+----------------------------------+|
		+------------------------------------+
		"""
		self.main_widget = QtWidgets.QFrame(self)
		self.main_widget.setObjectName("main_widget")

		self.vertical_layout = QtWidgets.QVBoxLayout(self.main_widget)
		self.vertical_layout.setObjectName("vertical_layout")

		# Message title
		self.label_title = QtWidgets.QLabel("")
		self.label_title.setObjectName("label_title")
		self.label_title.setSizePolicy(
			QtWidgets.QSizePolicy.Preferred,
			QtWidgets.QSizePolicy.MinimumExpanding
		)

		# Separating line
		self.horizontal_line = QtWidgets.QLabel("")
		self.horizontal_line.setMaximumSize(QtCore.QSize(16777215, 1))
		self.horizontal_line.setObjectName("horizontal_line")

		# Message text
		self.label_message = QtWidgets.QLabel("")
		self.label_message.setObjectName("label_message")
		self.label_message.setSizePolicy(
			QtWidgets.QSizePolicy.Preferred,
			QtWidgets.QSizePolicy.MinimumExpanding
		)

		# Add them all to the layout
		self.vertical_layout.addWidget(self.label_title)
		self.vertical_layout.addWidget(self.horizontal_line)
		self.vertical_layout.addWidget(self.label_message)


	def paintEvent(self, event):
		"""Extend the paintEvent to draw a dark overlay over the parent
		widget.
		"""
		parent_size = self.parent().size()
		overlay = QtGui.QPainter(self)
		overlay.fillRect(
			0, 0,
			parent_size.width(), parent_size.height(),
			QtGui.QColor(0, 0, 0, 85)
		)


	def resizeEvent(self, event):
		"""Resize this widget according to parent's size."""

		self.resize(self.parent().size())


	def show_message(self, title, msg="", suffix=""):
		"""Populate title and message and show this widget.

		Args:
			title (str): Message title.
			msg (str, optional): Message message.
			suffix (str, optional): Title suffix.
		"""

		self.label_title.setText("{0} {1}".format(title, suffix))
		self.update_message(msg)
		self.setVisible(True)


	def update_message(self, msg):
		"""Update message, generally while the widget is displayed.

		Args:
			msg (str, optional): Message message.
		"""

		if msg != "":
			self.label_message.setText("{0}".format(msg))
			self.label_message.setVisible(True)

		self.update_widget()
		QtWidgets.QApplication.processEvents()


	def update_widget(self):
		"""Ensure the widget is the correct size and centered within its
		parent.
		"""
		self.main_widget.adjustSize()
		parent_size = self.parent().size()
		main_widget_size = self.main_widget.size()
		self.resize(parent_size)
		self.main_widget.move(
			(parent_size.width() - main_widget_size.width()) / 2,
			(parent_size.height() - main_widget_size.height()) / 2
		)


	def hide_message(self):
		"""Hide this widget."""

		self.setVisible(False)
		QtWidgets.QApplication.processEvents()


	def get_message(self):
		"""Return current message.

		Returns:
			str: Widget's message.
		"""
		return self.label_message.text()
