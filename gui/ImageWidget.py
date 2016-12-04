from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ImageWidget(QtGui.QWidget):
	def __init__(self, parent):
		super(ImageWidget, self).__init__(parent)
		self.Qimg = None

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		if self.Qimg:
			painter.drawImage(event.rect(), self.Qimg, event.rect())
		painter.end()