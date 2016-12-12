from PIL import Image
import PIL.ImageOps
import math
import numpy
import datetime
from PIL import ImageFile
from Modals import *

ImageFile.LOAD_TRUNCATED_IMAGES = True
# from datetime import datetime

class ImagePreProcessor(object):

	def __init__(self):
		self.image = None
		self.pixels = None
		self.modal_window = Modal()
		self.contrast_mod_value = 0


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
		if self.modal_window.exec_() == False:
			self.contrast_mod_value = self.modal_window.button_confirm_exit()
			# print("prepre " + str(self.contrast_mod_value))
			auto_contrast_img = PIL.ImageOps.autocontrast(self.image,int(self.contrast_mod_value))
			self.image = auto_contrast_img
			self.loadImageFromPIX(self.image)

	def auto_grayscale(self):
		grayscale_img = PIL.ImageOps.grayscale(self.image)
		self.image = grayscale_img
		self.loadImageFromPIX(self.image)

	def auto_colorize(self):
		# ma pracowac na zdjeciu w odcieniach szarosci
		colorize_img = PIL.ImageOps.colorize(self.image, black="#000099", white="#99CCFF")
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
		posterize_img = PIL.ImageOps.posterize(self.image, 2)
		self.image = posterize_img
		self.loadImageFromPIX(self.image)

	def auto_solarize(self):
		solarize_img = PIL.ImageOps.solarize(self.image, 32)
		self.image = solarize_img
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