import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#  mozna zmienic na QWidget
class Modal(QDialog):
	def __init__(self, parent = None):
		super(Modal, self).__init__(parent)
		self.setAttribute(Qt.WA_DeleteOnClose, False)
		self.slider = QSlider(Qt.Horizontal)
		self.slider_value = 0
		self.min_label = QLabel("0", parent)
		self.current_value_label = QLabel("Kontrast:  "+str(self.slider_value), parent)
		self.max_label = QLabel("50", parent)
		self.button_confirm = QPushButton("Zatwierdź")
		self.button_cancel = QPushButton("Anuluj")
		self.layout = QVBoxLayout()
		self.label_layout = QHBoxLayout()
		self.buttons_layout = QHBoxLayout()

		self.label_layout.addWidget(self.min_label)

		self.current_value_label.setAlignment(Qt.AlignCenter| Qt.AlignVCenter)
		self.slider.valueChanged.connect(self.get_slider_value)
		self.label_layout.addWidget(self.current_value_label)

		self.label_layout.addWidget(self.max_label)
		self.max_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

		self.layout.addLayout(self.label_layout)

		self.slider.setMinimum(0)
		self.slider.setMaximum(50)
		self.slider.setValue(25)
		self.slider.setTickInterval(1)

		self.layout.addWidget(self.slider)

		# self.button_confirm.setAlignment(Qt.AlignLeft| Qt.AlignVCenter)
		# self.button_cancel.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
		self.button_confirm.released.connect(self.button_confirm_exit)
		self.button_cancel.released.connect(self.button_cancel_exit)

		self.buttons_layout.addWidget(self.button_confirm)
		self.buttons_layout.addWidget(self.button_cancel)
		self.layout.addLayout(self.buttons_layout)

		self.setLayout(self.layout)
		self.setGeometry(QRect(50, 50, 400, 100))
		self.setWindowTitle("Zmiana kontrastu")

	def get_slider_value(self):
		self.slider_value = self.slider.value()
		self.current_value_label.setText(str("Kontrast:  "+str(self.slider_value)))

	def button_confirm_exit(self):
		# print("modak "+str(self.slider_value))
		self.close()
		return self.slider_value

	def button_cancel_exit(self):
		self.close()