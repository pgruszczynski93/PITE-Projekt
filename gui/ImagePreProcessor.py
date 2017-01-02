import PIL.ImageOps
import PIL.ImageDraw
import PIL.ImageFont
import math
import numpy
import datetime
import matplotlib
import random
from PIL import ImageFile
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter

from Modals import *
from Histogram import *

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
		self.brightness_mod_value = 100
		self.width = 0
		self.height = 0
		self.enhancer = None
		self.colbalance_mod_value = 100
		self.mouse_pos = ()
		self.input_text = ""
		self.drawer = None
		self.font = None
		self.gaussian_radius = 0
		self.modalfilter_size = 0
		self.minfilter_size = 0
		self.maxfilter_size = 0
		self.medianfilter_size = 0
		self.rankfilter_size = 0
		self.unsharp_mod_values = ()
		self.kernel_vals = ()
		self.treshold_value = 0
		self.saturation_mod_value = 0
		self.gamma_mod_value = 0
		self.color_mod_value = 0
		self.noise_mod_value = 0
		self.marker_mod_values = None

	def set_mouse_pos(self, pos):
		self.mouse_pos = (pos[0], pos[1])

	def get_mouse_pos(self):
		return self.mouse_pos

	def loadImage(self, imgFile, isGray=1):
		self.image = Image.open(imgFile)
		self.width, self.height = self.image.size
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
		self.modal_window.set_slider(0,50,self.contrast_mod_value,1)
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
		self.modal_window.set_slider(0,8,self.posterize_mod_value,1)
		if self.modal_window.exec_() == False:
			self.posterize_mod_value = self.modal_window.button_confirm_exit()
			# print("prepre " + str(self.posterize_mod_value))
			posterize_img = PIL.ImageOps.posterize(self.image, self.posterize_mod_value)
			self.image = posterize_img
			self.loadImageFromPIX(self.image)

	def auto_solarize(self):
		self.modal_window = Modal("Próg solaryzacji: ")
		self.modal_window.init_modal(0,128,0,128,1,"Solaryzacja")
		self.modal_window.set_slider(0,128,self.solarization_mod_value,1)
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
		self.modal_window.set_slider(0,360,self.rotate_mod_angle,1)
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
			self.image = Image.new("RGBA",(int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1])),(255,255,255,255))
			self.loadImageFromPIX(self.image)


	def auto_brightness(self):
		self.modal_window = Modal("Jasność (%): ")
		self.modal_window.init_modal(0,200,0,200,1,"Zmiana jasności")
		self.modal_window.set_slider(0,200,self.brightness_mod_value,1)
		if self.modal_window.exec_() == False:
			self.enhancer = ImageEnhance.Brightness(self.image)
			# jct wstawic zmienna trzymajace wymiary po zmianie rozmiaru
			self.brightness_mod_value = self.modal_window.button_confirm_exit()
			self.image = self.enhancer.enhance(self.brightness_mod_value/100)
			# print(self.brightness_mod_value)
			self.loadImageFromPIX(self.image)


	def auto_colorbalance(self):
		self.modal_window = Modal("Stopień balansu (%): ")
		self.modal_window.init_modal(0,200,0,200,1,"Balans kolorów")
		self.modal_window.set_slider(0,200,self.colbalance_mod_value,1)
		if self.modal_window.exec_() == False:
			self.enhancer = ImageEnhance.Color(self.image)
			# jct wstawic zmienna trzymajace wymiary po zmianie rozmiaru
			self.colbalance_mod_value = self.modal_window.button_confirm_exit()
			self.image = self.enhancer.enhance(self.colbalance_mod_value/100)
			# print(self.brightness_mod_value)
			self.loadImageFromPIX(self.image)

	def auto_filter(self, selected_filter):
		filtered_img = self.image.filter(selected_filter)
		self.image = filtered_img
		self.loadImageFromPIX(self.image)

	def auto_add_text(self):
		# poprawić dodawanie tekstu - zdjecie ma byc w trybie rgba
		self.modal_window = Modal()
		self.modal_window.init_text_modal("Wprowadź tekst do wstawienia ")
		if self.modal_window.exec_() == False:
			txt = Image.new('RGBA', self.image.size, (255,255,255,255))

			self.input_text = self.modal_window.button_text_confirm_exit()
			text_color = self.modal_window.init_color_picker_mode("Kolor tekstu")
			self.font = PIL.ImageFont.truetype("arial.ttf", 15)
			# print(self.input_text)
			self.drawer = PIL.ImageDraw.Draw(txt)
			self.drawer.text((self.mouse_pos[0],self.mouse_pos[1]), self.input_text, font=self.font, fill= text_color)
			tmp_out = Image.alpha_composite(self.image, txt)
			self.image = tmp_out
			self.loadImageFromPIX(self.image)

	def auto_gaussianblur(self):
		self.modal_window = Modal("Promień rozmycia: ")
		self.modal_window.init_modal(0,10,0,10,1,"Rozmycie Gaussa")
		self.modal_window.set_slider(0,10,self.gaussian_radius,10)
		if self.modal_window.exec_() == False:
			self.gaussian_radius  = self.modal_window.button_confirm_exit()
			gaussianblurred_img =self.image.filter(ImageFilter.GaussianBlur(self.gaussian_radius))
			self.image = gaussianblurred_img
			self.loadImageFromPIX(self.image)

	def auto_unsharpmask(self):
		self.modal_window = Modal()
		self.modal_window.init_unsharp_mask("Maska wyostrzająca")
		self.modal_window.set_unsharp_sliders(self.unsharp_mod_values)
		if self.modal_window.exec_() == False:
			self.unsharp_mod_values  = self.modal_window.button_unsharpmasking_confirm()
			# print(self.unsharp_mod_values)
			unsharp_img =self.image.filter(ImageFilter.UnsharpMask(self.unsharp_mod_values[0],self.unsharp_mod_values[1],self.unsharp_mod_values[2]))
			self.image = unsharp_img
			self.loadImageFromPIX(self.image)


	def auto_kernel(self):
		self.modal_window = Modal()
		self.modal_window.init_combobox_ownmask("Zdefiniuj maskę")
		if self.modal_window.exec_() == False:
			self.kernel_vals  = self.modal_window.button_ownmask_confirm()
			kernel_img =self.image.filter(ImageFilter.Kernel(self.kernel_vals[0], self.kernel_vals[1]))
			# kernel_img =self.image.filter(ImageFilter.Kernel(self.kernel_vals[0], [0,-1,0,-1,5,-1,0,-1,0]))
			print(self.kernel_vals[0], self.kernel_vals[1], type(self.kernel_vals[1][1]))
			self.image = kernel_img
			self.loadImageFromPIX(self.image)

	def auto_rankfilter(self):
		self.modal_window = Modal("Rozmiar rozmycia: ")
		self.modal_window.init_modal(1,15,1,15,2,"Filtr rankingowy")
		self.modal_window.set_slider(1,15,self.rankfilter_size,2)
		if self.modal_window.exec_() == False:
			self.rankfilter_size  = self.modal_window.button_confirm_exit()
			rank_img = self.image.filter(ImageFilter.RankFilter(self.rankfilter_size,int(self.rankfilter_size*self.rankfilter_size/2)))
			self.image = rank_img
			self.loadImageFromPIX(self.image)

	def auto_medianfilter(self):
		self.modal_window = Modal("Rozmiar rozmycia: ")
		self.modal_window.init_modal(1,15,1,15,2,"Filtr medianowy")
		self.modal_window.set_slider(1,15,self.medianfilter_size,2)
		if self.modal_window.exec_() == False:
			self.medianfilter_size  = self.modal_window.button_confirm_exit()
			median_img = self.image.filter(ImageFilter.MedianFilter(self.medianfilter_size))
			self.image = median_img
			self.loadImageFromPIX(self.image)
		
	def auto_minfilter(self):
		self.modal_window = Modal("Rozmiar rozmycia: ")
		self.modal_window.init_modal(1,15,1,15,2,"Filtr minimalny")
		self.modal_window.set_slider(1,15,self.minfilter_size,2)
		if self.modal_window.exec_() == False:
			self.minfilter_size  = self.modal_window.button_confirm_exit()
			minfilter_img = self.image.filter(ImageFilter.MinFilter(self.minfilter_size))
			self.image = minfilter_img
			self.loadImageFromPIX(self.image)

	def auto_maxfilter(self):
		self.modal_window = Modal("Rozmiar rozmycia: ")
		self.modal_window.init_modal(1,15,1,15,2,"Filtr maksymalny")
		self.modal_window.set_slider(1,15,self.maxfilter_size,2)
		if self.modal_window.exec_() == False:
			self.maxfilter_size  = self.modal_window.button_confirm_exit()
			maxfilter_img = self.image.filter(ImageFilter.MaxFilter(self.maxfilter_size))
			self.image = maxfilter_img
			self.loadImageFromPIX(self.image)

	def auto_modefilter(self):
		self.modal_window = Modal("Rozmiar rozmycia: ")
		self.modal_window.init_modal(0,10,0,10,1,"Filtr modalny")
		self.modal_window.set_slider(0,10,self.modalfilter_size,10)
		if self.modal_window.exec_() == False:
			self.modalfilter_size  = self.modal_window.button_confirm_exit()
			modalfilter_img =self.image.filter(ImageFilter.ModeFilter(self.modalfilter_size))
			self.image = modalfilter_img
			self.loadImageFromPIX(self.image)

	def pre_treshold(self):
		self.modal_window = Modal("Próg: ")
		self.modal_window.init_modal(0,255,0,255,1,"Progowanie")
		self.modal_window.set_slider(0,255,self.treshold_value,1)
		if self.modal_window.exec_() == False:
			self.treshold_value = self.modal_window.button_confirm_exit()
			self.image = self.treshold(self.treshold_value)
			self.loadImageFromPIX(self.image)

	def treshold(self, value):
		copy = self.image.copy()
		tup_value = (value,value,value)
		white = (255,255,255)
		black = (0,0,0)
		for w in range(self.width):
			for h in range(self.height):
				if(self.image.getpixel((w,h))>tup_value):
					copy.putpixel((w,h),white)
				else:
					copy.putpixel((w,h),black)
		return copy
		

	# ############################

	def saturation(self):
		self.modal_window = Modal("Stopień nasycenia (%): ")
		self.modal_window.init_modal(0,200,0,200,1,"Nasycenie")
		self.modal_window.set_slider(0,200,self.saturation_mod_value,1)
		if self.modal_window.exec_() == False:
			self.saturation_mod_value = self.modal_window.button_confirm_exit()
			in_data = numpy.asarray(self.image, dtype=numpy.uint8)
			in_data = in_data/255.
			hsv = matplotlib.colors.rgb_to_hsv(in_data)
			hsv[:,:,1] = hsv[:,:,1] - 1.0 + (self.saturation_mod_value/100.)
			for y in range(self.height):
				for x in range(self.width):
					if hsv[y,x,1] < 0:
						hsv[y,x,1] = 0.0
					elif hsv[y,x,1] > 1:
						hsv[y,x,1] = 1.0
			rgb = matplotlib.colors.hsv_to_rgb(hsv)
			rgb = rgb*255.9999
			rgb = numpy.uint8(rgb)
			self.image = Image.fromarray(rgb)
			self.loadImageFromPIX(self.image)
 
	def gamma_correction(self):
		self.modal_window = Modal("Wartość wspołczynnika: ")
		self.modal_window.init_modal(0.01,7.99,0.01,7.99,1,"Korekcja Gamma")
		self.modal_window.set_slider(1,799,self.gamma_mod_value,1)
		if self.modal_window.exec_() == False:
			self.gamma_mod_value = 1.0/(self.modal_window.button_confirm_exit()/100.0)
			in_data = numpy.asarray(self.image, dtype=numpy.uint8)
			in_data = in_data/255.
			in_data = in_data ** self.gamma_mod_value
			in_data = in_data*255.9999
			in_data = numpy.uint8(in_data)
			self.image = Image.fromarray(in_data)
			self.loadImageFromPIX(self.image)
 
	def color_change(self):
		self.modal_window = Modal("Zmiana koloru (%): ")
		self.modal_window.init_modal(0,360,0,360,1,"Koło barw")
		self.modal_window.set_slider(0,360,self.color_mod_value,1)
		if self.modal_window.exec_() == False:
			self.color_mod_value = self.modal_window.button_confirm_exit()
			in_data = numpy.asarray(self.image, dtype=numpy.uint8)
			in_data = in_data/255.
			hsv = matplotlib.colors.rgb_to_hsv(in_data)
			hsv[:,:,0] = hsv[:,:,0] + (self.color_mod_value/360.)
			hsv[:,:,0] = ((hsv[:,:,0]*100) % 100) /100. 
			rgb = matplotlib.colors.hsv_to_rgb(hsv)
			rgb = rgb*255.9999
			rgb = numpy.uint8(rgb)
			self.image = Image.fromarray(rgb)
			self.loadImageFromPIX(self.image)
 
	def noise_generator(self):
		self.modal_window = Modal("Zaszumienie (%): ")
		self.modal_window.init_modal(0,100,0,100,1,"Pieprz i sol")
		self.modal_window.set_slider(0,100,self.noise_mod_value,1)
		if self.modal_window.exec_() == False:
			self.noise_mod_value = self.modal_window.button_confirm_exit()
			in_data = numpy.asarray(self.image, dtype=numpy.uint8)
			in_data = in_data/255.
			for y in range(self.height):
				for x in range(self.width):
					if random.randint(0, 100) < self.noise_mod_value:
						if random.randint(0,1) == 0:
							in_data[y,x,0] = 0.0
							in_data[y,x,1] = 0.0
							in_data[y,x,2] = 0.0
						else:
							in_data[y,x,0] = 1.0
							in_data[y,x,1] = 1.0
							in_data[y,x,2] = 1.0
			in_data = in_data*255.9999
			in_data = numpy.uint8(in_data)
			self.image = Image.fromarray(in_data)
			self.loadImageFromPIX(self.image)
			
	def put_marker(self):
		self.modal_window = Modal()
		self.modal_window.init_markers_modal("Wstawianie markera")
		if self.modal_window.exec_() == False:
			self.marker_mod_values = self.modal_window.button_marker_confirm_exit()
			pos_width = int(self.marker_mod_values[0])
			pos_height = int(self.marker_mod_values[1])
			size = int(self.marker_mod_values[2])
			shape = int(self.marker_mod_values[3])
			kind = int(self.marker_mod_values[4])
			red = int(self.marker_mod_values[5])
			green = int(self.marker_mod_values[6])
			blue = int(self.marker_mod_values[7])

			in_data = numpy.asarray(self.image, dtype=numpy.uint8)
			in_data = in_data/255.
						
			if (pos_width - size < 0) or \
			(pos_width + size > self.width) or \
			(pos_height - size) < 0 or \
			(pos_height + size > self.height):
				self.modal_window.msg_box("Niewłaściwa pozycja markera bądź jego rozmiar.")
			else:
				if shape == 1:
					if kind == 1:
						for y in range(self.height):
							for x in range(self.width):
								if (abs(pos_width - x) < size) and \
								(abs(pos_height - y) < size):
									in_data[y,x,0] = red/255.
									in_data[y,x,1] = green/255.
									in_data[y,x,2] = blue/255.
					elif kind == 2:
						for y in range(self.height):
							for x in range(self.width):
								if (abs(pos_width - x) > size) or \
								(abs(pos_height - y) > size):
									in_data[y,x,0] = red/255.
									in_data[y,x,1] = green/255.
									in_data[y,x,2] = blue/255.
				elif shape == 2:
					if kind == 1:
						for y in range(self.height):
							for x in range(self.width):
								if ((((x-pos_width)*(x-pos_width)) + ((y-pos_height)*(y-pos_height))) < (size*size)):
									in_data[y,x,0] = red/255.
									in_data[y,x,1] = green/255.
									in_data[y,x,2] = blue/255.
					elif kind == 2:
						for y in range(self.height):
							for x in range(self.width):
								if ((((x-pos_width)*(x-pos_width)) + ((y-pos_height)*(y-pos_height))) > (size*size)):
									in_data[y,x,0] = red/255.
									in_data[y,x,1] = green/255.
									in_data[y,x,2] = blue/255.
				elif shape == 3:
					if kind == 1:
						for y in range(self.height):
							for x in range(self.width):
								if ((abs(pos_width - x) < (size/3)) and \
								(abs(pos_height - y) < size)) or\
								((abs(pos_width - x) < size) and \
								(abs(pos_height - y) < (size/3))):
									in_data[y,x,0] = red/255.
									in_data[y,x,1] = green/255.
									in_data[y,x,2] = blue/255.
					elif kind == 2:
						for y in range(self.height):
							for x in range(self.width):
								if ((abs(pos_width - x) > (size/3)) or \
								(abs(pos_height - y) > size)) and\
								((abs(pos_width - x) > size) or \
								(abs(pos_height - y) > (size/3))):
									in_data[y,x,0] = red/255.
									in_data[y,x,1] = green/255.
									in_data[y,x,2] = blue/255.

			in_data = in_data*255.9999
			in_data = numpy.uint8(in_data)
			self.image = Image.fromarray(in_data)
			self.loadImageFromPIX(self.image)

	# #################
	def sample_color(self):
		if self.mouse_pos[0] <= self.width and self.mouse_pos[1] <= self.height:
			pix = self.image.getpixel((self.mouse_pos[0],self.mouse_pos[1]))
			self.modal_window = Modal()
			self.modal_window.init_color_sampler(pix, "Wartość koloru (RGB)")
			self.modal_window.exec_()

	def show_histogram(self):
		hist = Histogram(self.image)
		hist.create_histogram()
		hist.draw_histogram()
		self.modal_window = Modal()
		self.modal_window.init_histogram_drawer(hist.get_hist_img(), "Histogram");
		self.modal_window.exec_()

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
