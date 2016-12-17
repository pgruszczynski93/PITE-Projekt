import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *	

#  mozna zmienic na QWidget
class Modal(QDialog):
	def __init__(self, window_opt="", parent = None):
		super(Modal, self).__init__(parent)
		self.setAttribute(Qt.WA_DeleteOnClose, False)
		self.slider = QSlider(Qt.Horizontal)
		self.slider_value = 0
		self.min_label = QLabel("0", parent)
		self.current_value_label = QLabel("", parent)
		self.max_label = QLabel("50", parent)
		self.button_confirm = QPushButton("Zatwierdź")
		self.button_cancel = QPushButton("Anuluj")
		self.layout = QVBoxLayout()
		self.label_layout = QHBoxLayout()
		self.label_layout_2 = QHBoxLayout()
		self.buttons_layout = QHBoxLayout()
		self.colorpicker_color = None
		self.colorpicker_state = False
		self.window_opt = window_opt
		self.width_label = QLabel("Szerokość ", parent)
		self.width_tf = QLineEdit()
		self.height_tf = QLineEdit()
		self.text_tf = QLineEdit()
		self.text_label = QLabel("", parent)
		self.height_label = QLabel("Wysokość ", parent)

	def init_color_picker(self):
		self.colorpicker_color = QColorDialog.getColor(Qt.white,self, "Wybierz odcień bieli" if self.colorpicker_state else "Wybierz odcień czerni").getRgb()
		self.colorpicker_state = not self.colorpicker_state 
		return self.colorpicker_color

	def init_color_picker_mode(self, title):
		self.colorpicker_color = QColorDialog.getColor(Qt.white,self, title).getRgb()
		return self.colorpicker_color

	def init_modal(self, min_label, max_label, min_slider, max_slider, ticks_slider, title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100):
		self.set_labels(min_label,max_label, self.window_opt+str(self.slider_value))

		self.label_layout.addWidget(self.min_label)

		self.current_value_label.setAlignment(Qt.AlignCenter| Qt.AlignVCenter)
		self.slider.valueChanged.connect(self.get_slider_value)
		self.label_layout.addWidget(self.current_value_label)

		self.label_layout.addWidget(self.max_label)
		self.max_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

		self.layout.addLayout(self.label_layout)

		self.set_slider(min_slider,max_slider, self.slider_value, ticks_slider)

		self.layout.addWidget(self.slider)

		self.setup_buttons()
		self.add_widgets_to_buttons()
	
		self.layout.addLayout(self.buttons_layout)

		self.setLayout(self.layout)
		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)

	def init_resize_modal(self, title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100):

		self.width_tf.setValidator(QIntValidator())
		self.height_tf.setValidator(QIntValidator())

		self.label_layout.addWidget(self.width_label)
		self.label_layout.addWidget(self.width_tf)
		self.label_layout.addWidget(QLabel("pix",None))
		self.label_layout_2.addWidget(self.height_label)
		self.label_layout_2.addWidget(self.height_tf)
		self.label_layout_2.addWidget(QLabel("pix",None))

		self.layout.addLayout(self.label_layout)
		self.layout.addLayout(self.label_layout_2)

		self.button_confirm.released.connect(self.button_resize_confirm_exit)
		self.button_cancel.released.connect(self.button_cancel_exit)
		self.add_widgets_to_buttons()

		self.layout.addLayout(self.buttons_layout)
		self.setLayout(self.layout)
		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)

	def init_text_modal(self, title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100):
		self.label_layout.addWidget(self.text_label)
		self.label_layout.addWidget(self.text_tf)
		self.layout.addLayout(self.label_layout)

		self.button_confirm.released.connect(self.button_text_confirm_exit)
		self.button_cancel.released.connect(self.button_cancel_exit)
		self.add_widgets_to_buttons()

		self.layout.addLayout(self.buttons_layout)
		self.setLayout(self.layout)
		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)


	def setup_buttons(self):
		self.button_confirm.released.connect(self.button_confirm_exit)
		self.button_cancel.released.connect(self.button_cancel_exit)

	def add_widgets_to_buttons(self):
		self.buttons_layout.addWidget(self.button_confirm)
		self.buttons_layout.addWidget(self.button_cancel)

	def set_labels(self, l_min, l_max, l_current):
		self.min_label.setText(str(l_min));
		self.max_label.setText(str(l_max))
		self.current_value_label.setText(str(l_current))

	def set_slider(self,s_min,s_max,s_current,s_tick):
		self.slider.setMinimum(s_min)
		self.slider.setMaximum(s_max)
		self.slider.setValue(s_current)
		self.slider.setTickInterval(s_tick)

	def get_slider_value(self, text):
		self.slider_value = self.slider.value()
		self.current_value_label.setText(self.window_opt+str(self.slider_value))

	def button_confirm_exit(self):
		# print("modak "+str(self.slider_value))
		self.close()
		return self.slider_value

	def button_resize_confirm_exit(self):
		# print("modak "+str(self.slider_value))
		self.close()
		return (self.width_tf.text(),self.height_tf.text())

	def button_cancel_exit(self):
		self.close()

	def button_text_confirm_exit(self):
		# print("modak "+str(self.slider_value))
		self.close()
		return self.text_tf.text()