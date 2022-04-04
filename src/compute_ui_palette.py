# Common elements
self.col['tooltip'] = QtGui.QColor('#111')
self.col['line'] = self.col['window'].darker(110)
self.col['mandatory'] = QtGui.QColor(252, 152, 103)
self.col['warning'] = QtGui.QColor(255, 216, 106)
self.col['inherited'] = QtGui.QColor(161, 239, 228)

if self.col['highlight'].lightness() < 136:
	self.col['highlighted-text'] = QtGui.QColor('#fff')
else:
	self.col['highlighted-text'] = QtGui.QColor('#000')

if self.col['tooltip'].lightness() < 136:
	self.col['tooltip-text'] = QtGui.QColor('#fff')
else:
	self.col['tooltip-text'] = QtGui.QColor('#000')

# Dark mode UI
if self.col['window'].lightness() < 128:
	# Text
	self.col['text'] = QtGui.QColor('#ccc')
	self.col['disabled'] = QtGui.QColor('#666')
	if self.col['window'].lightness() > 68:
		self.col['text'] = QtGui.QColor('#fff')
		self.col['disabled'] = QtGui.QColor('#999')

	# Backgrounds and borders
	self.col['button'] = self.color_offset(self.col['window'], +34)
	self.col['button-border'] = self.col['button']
	self.col['group-bg'] = self.col['window'].lighter(108)
	self.col['group-header'] = self.col['window'].lighter(150)
	self.col['tab-bg'] = self.col['window'].lighter(116)
	self.col['tab-border'] = self.col['window'].lighter(150)
	self.col['input-bg'] = self.color_offset(self.col['window'], -34)
	self.col['input-border'] = self.col['button']
	self.col['menu-bg'] = self.col['window'].darker(128)
	self.col['menu-border'] = self.col['menu-bg'].lighter(150)
	self.col['disabled-bg'] = self.col['window'].lighter(115)
	self.col['alternate'] = self.color_offset(self.col['input-bg'], 7)

# Light mode UI
else:
	# Text
	self.col['text'] = QtGui.QColor('#333')
	self.col['disabled'] = QtGui.QColor('#999')
	if self.col['window'].lightness() < 187:
		self.col['text'] = QtGui.QColor('#000')
		self.col['disabled'] = QtGui.QColor('#666')

	# Backgrounds and borders
	self.col['button'] = self.col['window'].darker(104)
	self.col['button-border'] = self.col['button'].darker(125)
	self.col['group-bg'] = self.col['window'].lighter(102)
	self.col['group-header'] = self.col['window'].darker(110)
	self.col['tab-bg'] = self.col['window'].lighter(104)
	self.col['tab-border'] = self.col['line']
	self.col['input-bg'] = self.color_offset(self.col['window'], 34)
	self.col['input-border'] = self.col['window'].darker(107)
	self.col['menu-bg'] = self.color_offset(self.col['window'], +17)
	self.col['menu-border'] = self.col['menu-bg'].darker(150)
	self.col['disabled-bg'] = self.col['window'].darker(105)
	self.col['alternate'] = self.col['input-bg'].darker(103)

# Widget states
# self.col['checked'] = self.color_offset(self.col['button'], -17)
self.col['hover'] = self.col['button'].lighter(110)
# self.col['checked'] = self.col['highlight'].lighter(125)
self.col['checked'] = self.color_offset(self.col['button'], -17)
self.col['pressed'] = self.col['button'].darker(115)
self.col['button-text'] = self.col['text']

# Compute icon theme colours
self.col['icon-normal'] = self.nearest(self.col['text'])
self.col['icon-disabled'] = self.nearest(self.col['disabled'])
self.col['icon-highlighted'] = self.nearest(self.col['highlighted-text'])
