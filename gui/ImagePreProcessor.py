from PIL import Image
import math
import numpy

class ImagePreProcessor(object):

	def __init__(self):
		self.image = None
		self.pixels = None

	def loadImage(self, imgFile, isGray=1):
		self.image = Image.open(imgFile)
		self.pixels = self.image.load()

	def loadImageFromPIX(self, image):
		self.image = image
        # self.findHistogram()

	def negative(self):
		width, height =  self.image.size
		for i in range(width):
			for j in range(height):
				self.pixels[i,j] = 255 - int(self.pixels[i,j])
				# print(self.pixels[i,j])

		self.loadImageFromPIX(self.image)