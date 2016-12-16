from PIL import ImageFile
from PIL import Image
import PIL.ImageOps
import math
import numpy
import datetime
from Modals import *

ImageFile.LOAD_TRUNCATED_IMAGES = True
# from datetime import datetime

class ImagePreProcessor(object):

	def __init__(self):
		self.image = None
		self.pixels = None
		self.modal_window = None
		self.contrast_mod_value = 0
		self.posterize_mod_value = 0
		self.solarization_mod_value = 0
		self.crop_opsborder_mod_value = 0
		self.frame_color_width = 0
		self.resize_mod_dim = ()
		self.rotate_mod_angle = 0

	def loadImage(self, imgFile, isGray=1):
		self.image = Image.open(imgFile)
		self.pixels = self.image.load()

	def loadImageFromPIX(self, image):
		self.image = image

	def negative(self):
		inverted_image = PIL.ImageOps.invert(self.image)
		self.image = inverted_image
		self.loadImageFromPIX(self.image)

	def auto_contrast(self):
		# pobawic sie ta wartoscia jako drugi argument, jeszcze 3ci opcjonalny
		# false bo inaczej nie dziala XDD
		self.modal_window = Modal("Kontrast: ")
		self.modal_window.init_modal(0,50,0,50,1,"Zmiana kontrastu")
		if self.modal_window.exec_() == False:
			self.contrast_mod_value = self.modal_window.button_confirm_exit()
			# print("prepre " + str(self.contrast_mod_value))
			auto_contrast_img = PIL.ImageOps.autocontrast(self.image,int(self.contrast_mod_value))
			self.image = auto_contrast_img
			self.loadImageFromPIX(self.image)

		# chamskie ale sprawdzenie
		# del(self.modal_window) 

	def auto_grayscale(self):
		grayscale_img = PIL.ImageOps.grayscale(self.image)
		self.image = grayscale_img
		self.loadImageFromPIX(self.image)

	def auto_colorize(self):
		# ma pracowac na zdjeciu w odcieniach szarosci
		self.modal_window = Modal()
		black = self.modal_window.init_color_picker()
		white = self.modal_window.init_color_picker()
		colorize_img = PIL.ImageOps.colorize(self.image, black, white)
		self.image = colorize_img
		self.loadImageFromPIX(self.image)

	def auto_mirror(self):
		mirror_img = PIL.ImageOps.mirror(self.image)
		self.image = mirror_img
		self.loadImageFromPIX(self.image)

	def auto_flip(self):
		flip_img = PIL.ImageOps.flip(self.image)
		self.image = flip_img
		self.loadImageFromPIX(self.image)

	def auto_posterize(self):
		# ustawić prog posteryzacji jakims suwakeim - to samo solaryzacja
		self.modal_window = Modal("Bity kanałów: ")
		self.modal_window.init_modal(1,8,1,8,1,"Posteryzacja")
		if self.modal_window.exec_() == False:
			self.posterize_mod_value = self.modal_window.button_confirm_exit()
			# print("prepre " + str(self.posterize_mod_value))
			posterize_img = PIL.ImageOps.posterize(self.image, self.posterize_mod_value)
			self.image = posterize_img
			self.loadImageFromPIX(self.image)

	def auto_solarize(self):
		self.modal_window = Modal("Próg solaryzacji: ")
		self.modal_window.init_modal(0,128,0,128,1,"Solaryzacja")
		if self.modal_window.exec_() == False:
			self.solarization_mod_value = self.modal_window.button_confirm_exit()
			solarize_img = PIL.ImageOps.solarize(self.image, self.solarization_mod_value)
			self.image = solarize_img
			self.loadImageFromPIX(self.image)

	def auto_delete_border(self):
		self.modal_window = Modal("Piksele do usunięcia: ")
		self.modal_window.init_modal(0,200,0,200,1,"Usuwanie ramki zdjęcia")
		if self.modal_window.exec_() == False:
			self.crop_opsborder_mod_value = self.modal_window.button_confirm_exit()
			crop_img = PIL.ImageOps.crop(self.image, self.crop_opsborder_mod_value)
			self.image = crop_img
			self.loadImageFromPIX(self.image)

	def auto_equalize_histogram(self):
		# ewentualnie dodać maske jako drugi argument
		equal_hist_img = PIL.ImageOps.equalize(self.image)
		self.image = equal_hist_img
		self.loadImageFromPIX(self.image)

	def auto_add_color_border(self):
		self.modal_window = Modal("Grubość ramki: ")
		self.modal_window.init_modal(0,200,0,200,1,"Kolorowa ramka zdjęcia")
		if self.modal_window.exec_() == False:
			self.frame_color_width = self.modal_window.button_confirm_exit()
			frame_color = self.modal_window.init_color_picker()
			framed_img = PIL.ImageOps.expand(self.image, self.frame_color_width, frame_color)
			self.image = framed_img
			self.loadImageFromPIX(self.image)

	def auto_fitscale(self):
		self.modal_window = Modal()
		self.modal_window.init_resize_modal("Skalowanie i dopasowanie")
		if self.modal_window.exec_() == False:
			self.resize_mod_dim = self.modal_window.button_resize_confirm_exit()
			# sprawdzenie dla fit zmienic ew Image.resize
			resized_img = PIL.ImageOps.fit(self.image, (int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1])))
			self.image = resized_img
			# print(self.resize_mod_dim[0],self.resize_mod_dim[1])
			self.loadImageFromPIX(self.image)

	def auto_rotate(self):
		self.modal_window = Modal("Kąt obrotu: ")
		self.modal_window.init_modal(0,360,0,360,1,"Rotacja")
		if self.modal_window.exec_() == False:
			self.rotate_mod_angle = self.modal_window.button_confirm_exit()
			self.loadImageFromPIX(self.image.rotate(self.rotate_mod_angle,0,1))


	def auto_resize(self):
		self.modal_window = Modal()
		self.modal_window.init_resize_modal("Zmiana rozmiaru")
		if self.modal_window.exec_() == False:
			# jct wstawic zmienna trzymajace wymiary po zmianie rozmiaru
			self.resize_mod_dim = self.modal_window.button_resize_confirm_exit()
			self.loadImageFromPIX(self.image.resize((int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1]))))

	def	auto_new(self):
		self.modal_window = Modal()
		self.modal_window.init_resize_modal("Wymiary nowego pliku")
		if self.modal_window.exec_() == False:
			# jct wstawic zmienna trzymajace wymiary po zmianie rozmiaru
			self.resize_mod_dim = self.modal_window.button_resize_confirm_exit()
			self.image = Image.new("RGB",(int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1])),(255,255,255))
			self.loadImageFromPIX(self.image)


	def save_photo_normal(self):
		# domyslny zapis zdjecia pod skrótem ctrl+s
		if self.image:
			self.image.save(str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S"))+".jpg")
			message = "Zapisano pomyślnie w katalogu z programem"
		else:
			message = "Bład zapisu zdjęcia."

		return message

	def save_as(self, filepath):
		if self.image:
			self.image.save(filepath)
		else:
			return "Błąd zapisu zdjęcia"