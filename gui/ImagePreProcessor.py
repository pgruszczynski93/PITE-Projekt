from PIL import Image
import PIL.ImageOps
import math
import numpy
import datetime
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# from datetime import datetime

class ImagePreProcessor(object):

	def __init__(self):
		self.image = None
		self.pixels = None

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
		auto_contrast_img = PIL.ImageOps.autocontrast(self.image,40)
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