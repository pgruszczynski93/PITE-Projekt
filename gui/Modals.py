import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *	
from ImageWidget import *

class Modal(QDialog):
	def __init__(self, title="", window_opt="", frame_xlu=50, frame_ylu=50, frame_xrd=400, frame_yrd=100, parent=None):
		super(Modal, self).__init__(parent)
		self.setAttribute(Qt.WA_DeleteOnClose, False)
		self.main_slider = QSlider(Qt.Horizontal)
		self.main_slider_value = 0
		self.mask_size = 0
		self.width_tf = QLineEdit()
		self.height_tf = QLineEdit()
		self.text_tf = QLineEdit()
		self.sliders = []
		self.labels2 = [] 
		self.buttons = []
		self.textfields = []
		self.comboboxes = []
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
	def init_modal(self, label_vals, slider_opts):
		self.set_labels_with_list(self.labels2,label_vals)
		self.set_current_label_val(self.window_opt+str(self.main_slider_value))
		self.set_main_gridlayout(self.labels2,self.main_slider, None, None, None, None, None)
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
		self.setLayout(self.main_layout)

	def init_color_sampler(self, pixel):
		self.clear_list(self.labels2)
		self.set_labels_with_list(self.labels2, ["R: "+str(pixel[0]), "G: "+str(pixel[1]), "B: "+str(pixel[2])], "colorpipette")
		self.set_main_gridlayout(self.labels2,None,"colorpipette", None, None, None, None)
		self.append_to_mainlayout(self.main_gridlayout, self.main_layout)
		self.set_buttons(self.buttons,["OK"])
		self.setLayout(self.main_layout)

	def init_text_modal(self):
		self.add_widgets_to_layout(self.main_layout, [self.text_tf])
		self.set_buttons(self.buttons,["Zatwierdź","Anuluj"])
		self.setLayout(self.main_layout)

	def init_unsharp_mask(self):
		self.create_set_objects(self.sliders,3)
		self.set_main_gridlayout(None, None, "unsharp", None, None, None, None)
		self.set_slider(self.sliders[0],0,10,0,1)
		self.set_slider(self.sliders[1],0,200,0,1)
		self.set_slider(self.sliders[2],0,10,0,1)
		self.sliders[0].valueChanged.connect(lambda: self.set_current_label_val(self.sliders[0].value(),self.labels2[0],"Promień: "))
		self.sliders[1].valueChanged.connect(lambda: self.set_current_label_val(self.sliders[1].value(),self.labels2[1],"Procent: "))
		self.sliders[2].valueChanged.connect(lambda: self.set_current_label_val(self.sliders[2].value(),self.labels2[2],"Próg: "))
		self.append_to_mainlayout(self.main_gridlayout, self.main_layout)
		self.set_buttons(self.buttons,["Zatwierdź","Anuluj"])
		self.main_layout.addLayout(self.main_gridlayout)
		self.setLayout(self.main_layout)

	def init_own_mask_modal(self, size):
		if size:
			self.mask_size = size
			for i in range(self.mask_size*self.mask_size) :
				self.textfields.append(QLineEdit())
			self.set_main_gridlayout(None,None,"kernel",self.mask_size, None, None, None)
			self.append_to_mainlayout(self.main_gridlayout, self.main_layout)
			self.set_buttons(self.buttons,["Zatwierdź","Anuluj"])
			self.setLayout(self.main_layout)

	def init_markers_modal(self):
		self.set_labels_with_list(self.labels2,["Pozycja (S)zerokość: ","Pozycja (W)ysokość: ","Kształt: ","Rozmiar[pix]: ","Kolor: ","Rodzaj wypełnienia: "],"marker")
		self.create_set_objects(self.textfields, 3, "textfield")
		self.create_set_objects(self.comboboxes, 2, "combobox")
		self.comboboxes[0].addItems(["Kształt markera","Kwadrat","Koło","Krzyż"])
		self.comboboxes[1].addItems(["Wypełnienie","Wewnętrzne","Zewnętrzne"])
		self.set_main_gridlayout(self.labels2,None,"marker",None,self.textfields, self.comboboxes, None)
		self.append_to_mainlayout(self.main_gridlayout, self.main_layout)
		self.set_buttons(self.buttons,["Zatwierdź","Anuluj"])
		self.setLayout(self.main_layout)
		self.setGeometry(QRect(50,50,400,100))
# SETTERS, GETTERS AND OTHER
	def append_objects_to_list(self, object_name, objects,default_list):
		# object_type = self.object_names_types[str(object_name)]
		# for obj in objects:
			# default_list.append(object_type)
		pass

	def marker_color_picker(self):
		self.colorpicker_color = QColor(QColorDialog.getColor(Qt.black,self, "Wybierz odcień markera"))

	def create_set_objects(self, objects, object_num, object_type = None):
		to_append = None
		for i in range(object_num):
			if object_type == None:
				to_append = QSlider(Qt.Horizontal)
			elif object_type == "textfield":
				to_append = QLineEdit()
			elif object_type == "combobox":
				to_append = QComboBox()
			objects.append(to_append)
		
		for obj in objects:
			if object_type == None:
				obj.setValue(0)
			if object_type == "textfield":
				obj.setValidator(QIntValidator())
			if object_type == "combobox":
				pass

	def set_buttons(self, buttons, labels):
		for i, label in enumerate(labels):
			buttons.append(QPushButton(label,None))
		self.setup_buttons(buttons)
		self.add_widgets_to_layout(self.main_buttonhorlayout, buttons)
		self.append_to_mainlayout(self.main_buttonhorlayout, self.main_layout)

	def append_to_mainlayout(self, layout_to_insert, main_layout):
		main_layout.addLayout(layout_to_insert)

	def set_main_gridlayout(self,labels, slider=None, gridtype = None, size = None, textfields = None, comboboxes = None, buttons = None):
		if gridtype is None:
			for i,label in enumerate(labels):
				self.main_gridlayout.addWidget(label,0,i,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(slider,1,1)
			slider.valueChanged.connect(self.get_mainslider_value)
		elif gridtype == "colorpipette":
			for i,label in enumerate(labels):
				self.main_gridlayout.addWidget(label,i,0,(Qt.AlignHCenter))
		elif gridtype == "unsharp":
			labels = []
			self.clear_list(self.labels2)
			val_labels = [(QLabel("0", None), QLabel("10",None)),(QLabel("0", None), QLabel("200",None)),(QLabel("0", None), QLabel("10",None))]
			self.set_labels_with_list(self.labels2,["Promien: 0","Procent: 0","Prog: 0"],"unsharp")
			i = 0
			for j in range(0,6,2):
				self.main_gridlayout.addWidget(val_labels[i][0], j+1,0)
				self.main_gridlayout.addWidget(self.labels2[i], j,1)
				self.main_gridlayout.addWidget(val_labels[i][1], j+1,2)
				self.main_gridlayout.addWidget(self.sliders[i], j+1 ,1)
				self.labels2[i].setAlignment(Qt.AlignHCenter)
				val_labels[i][0].setAlignment(Qt.AlignHCenter)
				val_labels[i][1].setAlignment(Qt.AlignHCenter)
				i+=1
		elif gridtype == "kernel":
			for i in range(size):
				for j in range(size):
					self.main_gridlayout.addWidget(self.textfields[i*size+j],i,j)
					self.textfields[i*size+j].setValidator(QIntValidator())
		elif gridtype == "marker":
			button = QPushButton("Wybierz odcień")
			button.clicked.connect(self.marker_color_picker)
			self.main_gridlayout.addWidget(labels[0],0,0,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(textfields[0],0,1,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(labels[1],0,2,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(textfields[1],0,3,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(labels[3],1,0,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(textfields[2],1,1,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(labels[4],1,2,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(button,1,3,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(labels[2],2,0,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(comboboxes[0],2,1,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(labels[5],2,2,(Qt.AlignHCenter))
			self.main_gridlayout.addWidget(comboboxes[1],2,3,(Qt.AlignHCenter))
			
	def clear_list(self, list_to_clear):
		list_to_clear[:] = []

	def set_current_label_val(self, value, label = None, text = None):
		if label == None and text == None:
			self.current_value_label.setText(value)
		else: 
			label.setText(text+str(value))
			self.set_modal_return_value((self.sliders[0].value(),self.sliders[1].value(),self.sliders[2].value()))

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

	def set_sliders(self, sliders, value):
		for i, slider in enumerate(sliders):
			slider.setValue(value[i])

	def get_sliders(self):
		return self.sliders

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
		self.done(1)
		return self.get_modal_return_value()

	def button_nonsignal_confirm_exit(self, return_type = None):
		self.done(1)
		if return_type == None:
			self.set_modal_return_value((self.width_tf.text(),self.height_tf.text()))	
		elif return_type == "unsharp":
			self.set_modal_return_value(((self.mask_size,self.mask_size), [int(textfield.text()) for textfield in self.textfields]))
		elif return_type == "text":
			self.set_modal_return_value(self.text_tf.text())
		elif return_type == "marker":
			self.set_modal_return_value((self.textfields[0].text(),self.textfields[1].text(), self.textfields[2].text(), self.comboboxes[0].currentIndex(), \
			self.comboboxes[1].currentIndex(), QColor.red(self.colorpicker_color), QColor.green(self.colorpicker_color), QColor.blue(self.colorpicker_color)))
		return self.get_modal_return_value()

	def button_cancel_exit(self):
		self.done(0)
		self.close()

	def get_mainslider_value(self, text):
		self.main_slider_value = self.main_slider.value()
		self.current_value_label.setText(self.window_opt+str(self.main_slider_value))
		self.set_modal_return_value(self.main_slider_value)

	def msg_box(self, text):
		msgBox = QMessageBox()
		msgBox.setWindowTitle("Błąd")
		msgBox.setText(text)
		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec_()