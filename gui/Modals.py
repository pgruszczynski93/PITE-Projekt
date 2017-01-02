import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *	
from ImageWidget import *

#  mozna zmienic na QWidget
class Modal(QDialog):
	def __init__(self, window_opt="", parent = None):
		super(Modal, self).__init__(parent)
		self.setAttribute(Qt.WA_DeleteOnClose, False)
		# do przerobienia po refaktoryzacji
		# sprawdzić jak stworzyc kontenery ktore czyszcza sie po wyjsciu
		self.sliders = []
		self.labels2 = [] 
		self.layouts = []
		self.buttons = []
		self.textfields = []
		self.histogram = None
		self.histogram_label = QLabel()
		# 

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
		self.gridlayout = QGridLayout()

		# potrzebne do unsharp masking - przemyslec inne rozwiazanie
		self.texts = ["Promień: ","Procent (%): ","Próg: "]
		self.labels = [QLabel(self.texts[0], None), QLabel(self.texts[1], None), QLabel(self.texts[2], None)]
		self.sliders = [QSlider(Qt.Horizontal), QSlider(Qt.Horizontal), QSlider(Qt.Horizontal)]
		self.val_labels = [(QLabel("0", None), QLabel("10",None)),(QLabel("0", None), QLabel("200",None)),(QLabel("0", None), QLabel("10",None))]
		self.own_mask = []
		self.own_mask_values = []
		self.own_mask_layout = QGridLayout()
		self.item_list = QComboBox()
		self.user_kernel_size = 0;

# Image do QImage
	def pil2pixmap(self,im):
		if im.mode == "RGB":
			pass
		elif im.mode == "L":
			im = im.convert("RGBA")
		data = im.convert("RGBA").tobytes("raw", "RGBA")
		qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
		pixmap = QtGui.QPixmap.fromImage(qim)
		return pixmap

	def init_histogram_drawer(self,histogram,title, frame_xlu=50, frame_ylu=50, frame_xrd=260, frame_yrd=100):
		self.histogram = histogram
		self.histogram_label.setPixmap(self.pil2pixmap(self.histogram))

		self.layout.addWidget(self.histogram_label)
		self.setLayout(self.layout)
		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)

	def init_color_picker(self):
		self.colorpicker_color = QColorDialog.getColor(Qt.white,self, "Wybierz odcień bieli" if self.colorpicker_state else "Wybierz odcień czerni").getRgb()
		self.colorpicker_state = not self.colorpicker_state 
		return self.colorpicker_color

	def init_combobox_ownmask(self,title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100):
		self.item_list.addItem("Rozmiar maski")
		self.item_list.addItem("Maska 3x3")
		self.item_list.addItem("Maska 5x5")
		self.layout.addWidget(self.item_list)

		# self.init_own_mask_modal(size,title)
		# !!!!!!!!!!!!!!!!!!!!!!!!POPRAWIC GENEROWNAIE TEGO OKNA W ZALEZNOSCI OD WYBORU!!!!!!!!!!!!!!!!!}
		self.user_kernel_size = (3 if self.item_list.currentText() == "Maska 3x3" else 5 if self.item_list.currentText() == "Maska 5x5" else 0)
		self.user_kernel_size = 3 #tymczasowo!!!!!!!!!!!!!!!
		self.item_list.currentIndexChanged[str].connect(lambda: self.init_own_mask_modal(3,title))
		# print("sasa %d"%size)
		# !!!!!!!!!!!!!!!!!!!!!!!!POPRAWIC GENEROWNAIE TEGO OKNA W ZALEZNOSCI OD WYBORU!!!!!!!!!!!!!!!!!}
		# !!!!!!!!!!!!!!!!!!!!!!!!POPRAWIC GENEROWNAIE TEGO OKNA W ZALEZNOSCI OD WYBORU!!!!!!!!!!!!!!!!!}
		# !!!!!!!!!!!!!!!!!!!!!!!!POPRAWIC GENEROWNAIE TEGO OKNA W ZALEZNOSCI OD WYBORU!!!!!!!!!!!!!!!!!}

		self.setLayout(self.layout)
		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)

	def init_color_sampler(self, pixel, title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100):
		
		self.create_labels(4, "Wartość koloru: ", "R:", "G:","B: ")
		self.set_labels_2(pixel, "R: "+str(pixel[0]), "G: "+str(pixel[1]), "B: "+str(pixel[2]))

		self.button_confirm.released.connect(self.button_cancel_exit)
		self.button_cancel.released.connect(self.button_cancel_exit)
		self.add_widgets_to_buttons()
		self.layout.addLayout(self.buttons_layout)
		self.setLayout(self.layout)
		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)

	def create_labels(self, count, *titles):
		for i in range(4):
			self.labels2.append(QLabel(titles[i],None))
			self.layout.addWidget(self.labels2[i])

#  PAMIETAC O LABELS_2 przy finalnej kalsie
	def set_labels_2(self, values, *texts):
		for i, text in enumerate(texts):
				self.labels2[i+1].setText(text)


	def init_own_mask_modal(self, size,  title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100):
		if size:
			for i in range(size*size) :
				self.own_mask.append(QLineEdit())

			# for i, value in enumerate(values):
				# self.sliders[i].setValue(value)
			for i in range(size):
				for j in range(size):
					self.own_mask_layout.addWidget(self.own_mask[i*size+j],i,j)
					self.own_mask[i*size+j].setValidator(QIntValidator())
					# print(i*size+j)

			self.layout.addLayout(self.own_mask_layout)

			self.button_confirm.released.connect(self.button_ownmask_confirm)
			self.button_cancel.released.connect(self.button_cancel_exit)
			self.add_widgets_to_buttons()

			self.layout.addLayout(self.buttons_layout)
			self.setLayout(self.layout)
			self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
			self.setWindowTitle(title)

	def button_ownmask_confirm(self):
		self.close()
		return ((self.user_kernel_size,self.user_kernel_size), [int(textfield.text()) for textfield in self.own_mask])

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

	def init_unsharp_mask(self,title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100):

		i = 0
		for j in range(0,6,2):
			self.gridlayout.addWidget(self.val_labels[i][0], j+1,0)
			self.gridlayout.addWidget(self.labels[i], j,1)
			self.gridlayout.addWidget(self.val_labels[i][1], j+1,2)
			self.gridlayout.addWidget(self.sliders[i], j+1 ,1)
			self.labels[i].setAlignment(Qt.AlignCenter| Qt.AlignHCenter)
			self.val_labels[i][0].setAlignment(Qt.AlignCenter| Qt.AlignHCenter)
			self.val_labels[i][1].setAlignment(Qt.AlignCenter| Qt.AlignHCenter)
			
			i+=1

		self.sliders[0].setMinimum(0)
		self.sliders[0].setMaximum(10)
		self.sliders[0].setValue(0)
		self.sliders[0].setTickInterval(1)
		self.sliders[1].setMinimum(0)
		self.sliders[1].setMaximum(200)
		self.sliders[1].setValue(0)
		self.sliders[1].setTickInterval(0)
		self.sliders[2].setMinimum(0)
		self.sliders[2].setMaximum(10)
		self.sliders[2].setValue(0)
		self.sliders[2].setTickInterval(1)

		# for k in range(3): - nie wiem czemu jak robie to identycznie w petli to nie dziala ;P inaczej lambda tylko dl aost wyrazenia
		# for k in range(3):
		self.sliders[0].valueChanged.connect(lambda: self.change_label_value(self.labels[0],self.texts[0],self.sliders[0].value()))
		self.sliders[1].valueChanged.connect(lambda: self.change_label_value(self.labels[1],self.texts[1],self.sliders[1].value()))
		self.sliders[2].valueChanged.connect(lambda: self.change_label_value(self.labels[2],self.texts[2],self.sliders[2].value()))

		self.gridlayout.addWidget(self.button_confirm,6,0)
		self.gridlayout.addWidget(self.button_cancel,6,2)

		self.button_confirm.released.connect(lambda: self.button_unsharpmasking_confirm())
		self.button_cancel.released.connect(self.button_cancel_exit)

		self.layout.addLayout(self.gridlayout)
		self.setLayout(self.layout)
		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)

	def change_label_value(self,label,text, value):
		label.setText(text+str(value))

	def set_unsharp_sliders(self, values):
		for i, value in enumerate(values):
			self.sliders[i].setValue(value)
		# sliders.setMinimum(s_min)
		# sliders.setMaximum(s_max)
		# sliders.setValue(s_current)
		# sliders.setTickInterval(s_tick)

	def get_sliders_values(*values):
		pass

	def button_unsharpmasking_confirm(self):
		self.close()
		return (self.sliders[0].value(),self.sliders[1].value(),self.sliders[2].value())

		#todoo layter
	def fill_grid_layout(self, size, *args):
		pass

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

