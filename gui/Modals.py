import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *	
from ImageWidget import *

#  mozna zmienic na QWidget
class Modal(QDialog):
	def __init__(self, title="", window_opt="", frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100, parent=None):
		super(Modal, self).__init__(parent)
		self.setAttribute(Qt.WA_DeleteOnClose, False)
		# REFACTOR
		# ################################
		self.main_slider = QSlider(Qt.Horizontal)
		self.main_slider_value = 0
		self.width_tf = QLineEdit()
		self.height_tf = QLineEdit()

		self.sliders = []
		self.labels2 = [] 
		self.buttons = []
		self.textfields = []
		self.descr_texts = []

		self.histogram = None
		self.histogram_label = QLabel()
		self.current_value_label = QLabel("", parent)
		self.main_layout = QVBoxLayout()
		self.main_gridlayout = QGridLayout()
		self.main_horlayout = QHBoxLayout()
		self.main_buttonhorlayout = QHBoxLayout()

		self.object_names_types = {"button":QPushButton(),"label":QLabel(),"textfield":QLineEdit(),"slider":QSlider(Qt.Horizontal)}
		self.window_opt = window_opt
		self.colorpicker_color = None
		self.colorpicker_state = False
		self.modal_return_value = None
		self.non_signal_value = None

		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)
		# ################################ 

		self.label_layout = QHBoxLayout()
		self.label_layout_2 = QHBoxLayout()
		# self.buttons_layout = QHBoxLayout()
		# self.width_label = QLabel("Szerokość ", parent)

		self.text_tf = QLineEdit()
		self.text_label = QLabel("", parent)

		self.size_tf = QLineEdit()
		self.marker_color = QColor(0,0,0)
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
		self.item_list2 = QComboBox()
		self.item_list3 = QComboBox()

	def pil2pixmap(self,im):
		if im.mode == "RGB":
			pass
		elif im.mode == "L":
			im = im.convert("RGBA")
		data = im.convert("RGBA").tobytes("raw", "RGBA")
		qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
		pixmap = QtGui.QPixmap.fromImage(qim)
		return pixmap

# INITS
# #####################################################

	def init_modal(self, label_vals, slider_opts):
		self.set_labels_with_list(self.labels2,label_vals)
		self.set_current_label_val(self.window_opt+str(self.main_slider_value))
		self.set_main_gridlayout(self.labels2,self.main_slider)
		self.set_slider(self.main_slider, slider_opts[0], slider_opts[1], self.main_slider_value, slider_opts[2])
		self.append_to_mainlayout(self.main_gridlayout, self.main_layout)
		self.set_buttons(self.buttons, ["Zatwierdź", "Anuluj"])
		self.setLayout(self.main_layout)

	def init_histogram_drawer(self,histogram):
		self.histogram = histogram
		self.histogram_label.setPixmap(self.pil2pixmap(self.histogram))
		self.add_widgets_to_layout(self.main_layout, [self.histogram_label])
		self.setGeometry(QRect(100,100,260,200))
		self.setLayout(self.main_layout)

	def init_color_picker(self, title = ""):
		if len(title) == 0:
			self.colorpicker_color = QColorDialog.getColor(Qt.white,self, "Wybierz odcień bieli" if self.colorpicker_state else "Wybierz odcień czerni").getRgb()
			self.colorpicker_state = not self.colorpicker_state 
		else:
			self.colorpicker_color = QColorDialog.getColor(Qt.white,self, title).getRgb()
		return self.colorpicker_color

	def init_resize_modal(self, label_texts):
		textfield_layout = QHBoxLayout()
		self.width_tf.setValidator(QIntValidator())
		self.height_tf.setValidator(QIntValidator())
		self.set_labels_with_list(self.labels2,label_texts)
		self.add_widgets_to_layout(self.main_horlayout,self.labels2)
		self.add_widgets_to_layout(textfield_layout,[self.height_tf, self.width_tf])
		self.append_to_mainlayout(self.main_horlayout,self.main_layout)
		self.append_to_mainlayout(textfield_layout,self.main_layout)
		self.set_buttons(self.buttons, ["Zatwierdź", "Anuluj"])
		self.set_non_signal_value(1)
		self.setLayout(self.main_layout)

	def init_color_sampler(self, pixel):
		self.clear_list(self.labels2)
		self.set_labels_with_list(self.labels2, ["R: "+str(pixel[0]), "G: "+str(pixel[1]), "B: "+str(pixel[2])], "colorpipette")
		self.set_main_gridlayout(self.labels2,None,"colorpipette")
		self.append_to_mainlayout(self.main_gridlayout, self.main_layout)
		self.set_buttons(self.buttons,["OK"])
		self.setLayout(self.main_layout)

	def init_text_modal(self):
		self.add_widgets_to_layout(self.main_layout, [self.text_tf])
		self.set_buttons(self.buttons,["Zatwierdź","Anuluj"])
		self.set_non_signal_value(2)
		# ################# TUTAJAAAAAAAAAAAAAAAAAAAAAAAAAAA
		self.setLayout(self.main_layout)

# SETTERS & GETTERS
# #####################################################
	def set_non_signal_value(self,value):
		self.non_signal_value = value

	def get_non_signal_value(self):
		return self.non_signal_value

	def append_objects_to_list(self, object_name, objects,default_list):
		# object_type = self.object_names_types[str(object_name)]
		# for obj in objects:
			# default_list.append(object_type)
		pass

	def set_buttons(self, buttons, labels):
		for i, label in enumerate(labels):
			buttons.append(QPushButton(label,None))

		self.setup_buttons(buttons)
		self.add_widgets_to_layout(self.main_buttonhorlayout, buttons)
		self.append_to_mainlayout(self.main_buttonhorlayout, self.main_layout)

	def append_to_mainlayout(self, layout_to_insert, main_layout):
		main_layout.addLayout(layout_to_insert)

	def set_main_gridlayout(self,labels, slider=None, gridtype = None):
		if gridtype is None:
			for i,label in enumerate(labels):
				self.main_gridlayout.addWidget(label,0,i,(Qt.AlignHCenter))

			self.main_gridlayout.addWidget(slider,1,1)
			slider.valueChanged.connect(self.get_mainslider_value)
		elif gridtype == "colorpipette":
			for i,label in enumerate(labels):
				self.main_gridlayout.addWidget(label,i,0,(Qt.AlignHCenter))

	def clear_list(self, list_to_clear):
		list_to_clear[:] = []

	def set_current_label_val(self, value):
		self.current_value_label.setText(value)

	def set_labels_with_list(self, labels, texts, usage = None):
		for i, text in enumerate(texts):
			labels.append(QLabel(str(text),None))
		if usage == None:
			labels.insert(1,self.current_value_label)
		elif len(usage) > 0:
			pass

	def set_slider(self,slider,s_min,s_max,s_current,s_tick):
		slider.setMinimum(s_min)
		slider.setMaximum(s_max)
		slider.setValue(s_current)
		slider.setTickInterval(s_tick)	

	def set_modal_return_value(self,value):
		self.modal_return_value = value

	def get_modal_return_value(self):
		return self.modal_return_value

	def get_slider(self):
		return self.main_slider

	def setup_buttons(self,buttons):
		if len(buttons) > 1:
			buttons[0].clicked.connect(self.button_confirm_exit)
			buttons[1].clicked.connect(self.button_cancel_exit)
		elif len(buttons) == 1:
			buttons[0].clicked.connect(self.button_confirm_exit)

	def add_widgets_to_layout(self,layout, objects):
		for obj in objects:
			layout.addWidget(obj)

	def button_confirm_exit(self):
		# print("modak "+str(self.slider_value))
		self.done(1)
		return self.get_modal_return_value()

	def button_nonsignal_confirm_exit(self):
		self.done(1)
		self.set_modal_return_value((self.width_tf.text(),self.height_tf.text()))
		return self.get_modal_return_value()

	def button_cancel_exit(self):
		self.done(0)
		self.close()

	def get_mainslider_value(self, text):
		self.main_slider_value = self.main_slider.value()
		self.current_value_label.setText(self.window_opt+str(self.main_slider_value))
		self.set_modal_return_value(self.main_slider_value)

# ZMIENIC WSZYSTKIE METODY BUTTONOW NA JEDEN z GETSETMODALRETURN

	def button_text_confirm_exit(self):
		# print("modak "+str(self.slider_value))
		self.close()
		return self.text_tf.text()


	def button_marker_confirm_exit(self):
		self.close()
		return (self.width_tf.text(),self.height_tf.text(), self.size_tf.text(), self.item_list2.currentIndex(), \
		self.item_list3.currentIndex(), QColor.red(self.marker_color), QColor.green(self.marker_color), QColor.blue(self.marker_color))


	def button_ownmask_confirm(self):
		self.close()
		return ((self.user_kernel_size,self.user_kernel_size), [int(textfield.text()) for textfield in self.own_mask])


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	

	def init_marker_color_picker(self):
		self.marker_color = QColor(QColorDialog.getColor(Qt.black,self, "Wybierz odcień markera"))

	def init_combobox_ownmask(self,title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100):
		self.item_list.addItem("Rozmiar maski")
		self.item_list.addItem("Maska 3x3")
		self.item_list.addItem("Maska 5x5")
		self.main_layout.addWidget(self.item_list)

		# self.init_own_mask_modal(size,title)
		# !!!!!!!!!!!!!!!!!!!!!!!!POPRAWIC GENEROWNAIE TEGO OKNA W ZALEZNOSCI OD WYBORU!!!!!!!!!!!!!!!!!}
		self.user_kernel_size = (3 if self.item_list.currentText() == "Maska 3x3" else 5 if self.item_list.currentText() == "Maska 5x5" else 0)
		self.user_kernel_size = 3 #tymczasowo!!!!!!!!!!!!!!!
		self.item_list.currentIndexChanged[str].connect(lambda: self.init_own_mask_modal(3,title))
		# print("sasa %d"%size)
		# !!!!!!!!!!!!!!!!!!!!!!!!POPRAWIC GENEROWNAIE TEGO OKNA W ZALEZNOSCI OD WYBORU!!!!!!!!!!!!!!!!!}
		# !!!!!!!!!!!!!!!!!!!!!!!!POPRAWIC GENEROWNAIE TEGO OKNA W ZALEZNOSCI OD WYBORU!!!!!!!!!!!!!!!!!}
		# !!!!!!!!!!!!!!!!!!!!!!!!POPRAWIC GENEROWNAIE TEGO OKNA W ZALEZNOSCI OD WYBORU!!!!!!!!!!!!!!!!!}

		self.setLayout(self.main_layout)
		self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
		self.setWindowTitle(title)

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

			self.main_layout.addLayout(self.own_mask_layout)

			self.button_confirm.released.connect(self.button_ownmask_confirm)
			self.button_cancel.released.connect(self.button_cancel_exit)
			self.add_widgets_to_buttons()

			self.main_layout.addLayout(self.buttons_layout)
			self.setLayout(self.main_layout)
			self.setGeometry(QRect(frame_xlu, frame_ylu, frame_xrd, frame_yrd))
			self.setWindowTitle(title)

	def init_markers_modal(self, title, frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=400):

		self.width_tf.setValidator(QIntValidator())
		self.height_tf.setValidator(QIntValidator())

		layout1 = QHBoxLayout();
		layout2 = QHBoxLayout();
		layout3 = QHBoxLayout();
		layout4 = QHBoxLayout();
		layout5 = QHBoxLayout();
		layout6 = QHBoxLayout();
		layout7 = QHBoxLayout();
		layout8 = QHBoxLayout();
		layout9 = QHBoxLayout();
		layout10 = QHBoxLayout();

		layout1.addWidget(QLabel("Pozycja:",None))

		layout2.addWidget(self.width_label)
		layout2.addWidget(self.width_tf)
		layout2.addWidget(self.height_label)
		layout2.addWidget(self.height_tf)

		layout3.addWidget(QLabel("Kształt:",None))

		self.item_list2.addItem("Kształt markera")
		self.item_list2.addItem("Kwadrat")
		self.item_list2.addItem("Koło")
		self.item_list2.addItem("Krzyż")
		layout4.addWidget(self.item_list2)

		layout5.addWidget(QLabel("Rozmiar:",None))

		layout6.addWidget(QLabel("Pix",None))
		layout6.addWidget(self.size_tf)

		layout7.addWidget(QLabel("Kolor:",None))

		button = QPushButton("Wybierz odcień")
		button.clicked.connect(self.init_marker_color_picker)
		layout8.addWidget(button)		

		layout9.addWidget(QLabel("Rodzaj wypełnienia:",None))

		self.item_list3.addItem("Wypełnienie")
		self.item_list3.addItem("Zewnętrzne")
		self.item_list3.addItem("Wewnętrzne")
		layout10.addWidget(self.item_list3)

		self.main_layout.addLayout(layout1)
		self.main_layout.addLayout(layout2)
		self.main_layout.addLayout(layout3)
		self.main_layout.addLayout(layout4)
		self.main_layout.addLayout(layout5)
		self.main_layout.addLayout(layout6)
		self.main_layout.addLayout(layout7)
		self.main_layout.addLayout(layout8)
		self.main_layout.addLayout(layout9)
		self.main_layout.addLayout(layout10)

		self.button_confirm.released.connect(self.button_resize_confirm_exit)
		self.button_cancel.released.connect(self.button_cancel_exit)
		self.add_widgets_to_buttons()

		self.main_layout.addLayout(self.buttons_layout)
		self.setLayout(self.main_layout)
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

		self.main_layout.addLayout(self.gridlayout)
		self.setLayout(self.main_layout)
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

	def button_unsharpmasking_confirm(self):
		self.close()
		return (self.sliders[0].value(),self.sliders[1].value(),self.sliders[2].value())

	def set_labels(self, l_min, l_max, l_current):
		self.min_label.setText(str(l_min));
		self.max_label.setText(str(l_max))
		self.current_value_label.setText(str(l_current))


	def msg_box(self, text):
		msgBox = QMessageBox()
		msgBox.setWindowTitle("Błąd")
		msgBox.setText(text)

		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec_()
