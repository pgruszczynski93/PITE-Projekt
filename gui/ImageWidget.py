from PyQt4 import QtCore, QtGui

class ImageWidget(QtGui.QWidget):
	def __init__(self, parent):
		super(ImageWidget, self).__init__(parent)
		self.Qimg = None

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		if self.Qimg:
			painter.drawImage(event.rect(), self.Qimg, event.rect())
		painter.end()
