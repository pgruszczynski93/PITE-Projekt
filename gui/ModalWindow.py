import sys
from PyQt4 import QtCore, QtGui

class MyPopup(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)

	def paintEvent(self, e):
	    dc = QPainter(self)
	    dc.drawLine(0, 0, 100, 100)
	    dc.drawLine(100, 0, 0, 100)
