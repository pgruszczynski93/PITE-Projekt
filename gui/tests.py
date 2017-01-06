import unittest
from ImagePreProcessor import *

class tests(unittest.TestCase):
  
	def setUp(self):
		self.imgProcessor = ImagePreProcessor()
    
	def test_init(self):
		print("Sprawdzenie, czy obiekt jest instancją klasy ImagePreProcessor")
		self.assertIsInstance(self.imgProcessor, ImagePreProcessor)

	def test_parameters(self):
		print("Sprawdzenie, czy domyślne parametry instancji klasy są prawidłowe")
		self.assertEqual(self.imgProcessor.image, None)
		self.assertEqual(self.imgProcessor.pixels, None)
		self.assertEqual(self.imgProcessor.modal_window, None)
		self.assertEqual(self.imgProcessor.contrast_mod_value, 0)
		self.assertEqual(self.imgProcessor.posterize_mod_value, 0)
		self.assertEqual(self.imgProcessor.solarization_mod_value, 0)
		self.assertEqual(self.imgProcessor.crop_opsborder_mod_value, 0)
		self.assertEqual(self.imgProcessor.frame_color_width, 0)
		self.assertEqual(self.imgProcessor.resize_mod_dim, ())
		self.assertEqual(self.imgProcessor.rotate_mod_angle, 0)
		self.assertEqual(self.imgProcessor.brightness_mod_value, 100)
		self.assertEqual(self.imgProcessor.width, 0)
		self.assertEqual(self.imgProcessor.height, 0)
		self.assertEqual(self.imgProcessor.enhancer, None)
		self.assertEqual(self.imgProcessor.colbalance_mod_value, 100)
		self.assertEqual(self.imgProcessor.mouse_pos, ())
		self.assertEqual(self.imgProcessor.input_text, "")
		self.assertEqual(self.imgProcessor.drawer, None)
		self.assertEqual(self.imgProcessor.font, None)
		self.assertEqual(self.imgProcessor.gaussian_radius, 0)
		self.assertEqual(self.imgProcessor.modalfilter_size, 0)
		self.assertEqual(self.imgProcessor.minfilter_size, 0)
		self.assertEqual(self.imgProcessor.maxfilter_size, 0)
		self.assertEqual(self.imgProcessor.medianfilter_size, 0)
		self.assertEqual(self.imgProcessor.rankfilter_size, 0)
		self.assertEqual(self.imgProcessor.unsharp_mod_values, ())
		self.assertEqual(self.imgProcessor.kernel_vals, ())
		self.assertEqual(self.imgProcessor.treshold_value, 0)
		self.assertEqual(self.imgProcessor.saturation_mod_value, 0)
		self.assertEqual(self.imgProcessor.gamma_mod_value, 0)
		self.assertEqual(self.imgProcessor.color_mod_value, 0)
		self.assertEqual(self.imgProcessor.noise_mod_value, 0)
		self.assertEqual(self.imgProcessor.marker_mod_values, None)

	def test_image_load(self):
		print("Sprawdzenie funkcji wczytującej obraz wejściowy")
		self.imgProcessor.loadImage("./image.jpg")



if __name__ == '__main__':
	unittest.main()
