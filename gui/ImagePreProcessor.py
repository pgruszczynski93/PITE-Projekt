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
		self.resize_mod_dim = (300, 200)
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
		self.hist = None
		self.gaussian_radius = 0
		self.modalfilter_size = 3
		self.minfilter_size = 3
		self.maxfilter_size = 3
		self.medianfilter_size = 3
		self.rankfilter_size = 3
		self.unsharp_mod_values = (10, 20, 30)
		self.kernel_vals = ()
		self.treshold_value = 20
		self.saturation_mod_value = 0
		self.gamma_mod_value = 0
		self.color_mod_value = 0
		self.noise_mod_value = 0
		self.marker_mod_values = (100, 100, 10, 1, 1, 255, 255, 255)

	def image_close(self):
		self.image.close()

	def set_width(self, width):
		self.width = width

	def set_height(self, height):
		self.height = height

	def set_mouse_pos(self, pos):
		self.mouse_pos = (pos[0], pos[1])

	def get_mouse_pos(self):
		return self.mouse_pos

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def loadImage(self, imgFile, isGray=1):
		self.image = Image.open(imgFile)
		self.width, self.height = self.image.size
		self.pixels = self.image.load()

	def set_sizes(self, new_image):
		self.width, self.height = new_image.size

	def get_sizes(self):
		return (self.width, self.height)

	def loadImageFromPIX(self, image):
		self.image = image

	def image_filter(self):
		pass

	def image_transform(self):
		pass

	def image_adjustment(self):
		pass

	def negative(self):
		inverted_image = PIL.ImageOps.invert(self.image)
		self.image = inverted_image
		self.loadImageFromPIX(self.image)

	def auto_contrast_exec(self):
		self.image = PIL.ImageOps.autocontrast(self.image,int(self.contrast_mod_value))
		self.loadImageFromPIX(self.image)

	def auto_contrast(self):
		self.modal_window = Modal("Zmiana kontrastu","Kontrast: ")
		self.modal_window.append_objects_to_list("button",2,2)
		self.modal_window.init_modal([0,50],[0,50,1])
		self.modal_window.set_slider(self.modal_window.get_slider(), 0,50,self.contrast_mod_value,1)
		if self.modal_window.exec_():
		# print(if self.modal_window.exec_():
			self.contrast_mod_value = self.modal_window.button_confirm_exit()
		self.auto_contrast_exec()
		

	def auto_grayscale(self):
		grayscale_img = PIL.ImageOps.grayscale(self.image)
		self.image = grayscale_img
		self.loadImageFromPIX(self.image)

	def auto_colorize_exec(self, black, white):
		self.image = PIL.ImageOps.colorize(self.image, black, white)
		self.loadImageFromPIX(self.image)

	def auto_colorize(self):
		self.modal_window = Modal()
		black = self.modal_window.init_color_picker()
		white = self.modal_window.init_color_picker()
		self.auto_colorize_exec(black, white)

	def auto_mirror(self):
		self.image = PIL.ImageOps.mirror(self.image)
		self.loadImageFromPIX(self.image)

	def auto_flip(self):
		self.image = PIL.ImageOps.flip(self.image)
		self.loadImageFromPIX(self.image)

	def auto_posterize_exec(self):
		self.image = PIL.ImageOps.posterize(self.image, self.posterize_mod_value)
		self.loadImageFromPIX(self.image)

	def auto_posterize(self):
		self.modal_window = Modal("Posteryzacja","Bity kanałów: ")
		self.modal_window.init_modal([1,8],[1,8,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,8,self.posterize_mod_value,1)
		
		if self.modal_window.exec_():
			self.posterize_mod_value = self.modal_window.button_confirm_exit()
		self.auto_posterize_exec()
		

	def auto_solarize_exec(self):
		self.image = PIL.ImageOps.solarize(self.image, self.solarization_mod_value)
		self.loadImageFromPIX(self.image)

	def auto_solarize(self):
		self.modal_window = Modal("Solaryzacja","Próg solaryzacji: ")
		self.modal_window.init_modal([0,128],[0,128,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,128,self.solarization_mod_value,1)
		if self.modal_window.exec_():
			self.solarization_mod_value = self.modal_window.button_confirm_exit()
		self.auto_solarize_exec()

	def auto_delete_border_exec(self):
		self.image = PIL.ImageOps.crop(self.image, self.crop_opsborder_mod_value)
		self.set_sizes(self.image)
		self.loadImageFromPIX(self.image)
		

	def auto_delete_border(self):
		self.modal_window = Modal("Usuwanie ramki zdjęcia","Piksele do usunięcia: ")
		self.modal_window.init_modal([0,200],[0,200,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,200,self.crop_opsborder_mod_value,1)
		if self.modal_window.exec_():
			self.crop_opsborder_mod_value = self.modal_window.button_confirm_exit()
		self.auto_delete_border_exec()

	def auto_equalize_histogram(self):
		self.image = PIL.ImageOps.equalize(self.image)
		self.loadImageFromPIX(self.image)

	def auto_add_color_border_exec(self, frame_color):
		self.image = PIL.ImageOps.expand(self.image, self.frame_color_width, frame_color)
		self.set_sizes(self.image)
		self.loadImageFromPIX(self.image)

	def auto_add_color_border(self):
		self.modal_window = Modal("Kolorowa ramka zdjęcia","Grubość ramki: ")
		self.modal_window.init_modal([0,200],[0,200,1])
		if self.modal_window.exec_():
			self.frame_color_width = self.modal_window.button_confirm_exit()
		frame_color = self.modal_window.init_color_picker()
		self.auto_add_color_border_exec(frame_color)
		

	def auto_fitscale_exec(self):
		self.image = PIL.ImageOps.fit(self.image, (int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1])))
		self.set_sizes(self.image)
		self.loadImageFromPIX(self.image)

	def auto_fitscale(self):
		self.modal_window = Modal("Skalowanie i dopasowanie")
		self.modal_window.init_resize_modal(["Wysokość (pix)", "Szerokość (pix)"])
		if self.modal_window.exec_():
			self.resize_mod_dim = self.modal_window.button_nonsignal_confirm_exit()
		self.auto_fitscale_exec()

	def auto_rotate_exec(self):
		self.set_sizes(self.image.rotate(self.rotate_mod_angle,0,1))
		self.loadImageFromPIX(self.image.rotate(self.rotate_mod_angle,0,1))

	def auto_rotate(self):
		self.modal_window = Modal("Rotacja","Kąt obrotu: ")
		self.modal_window.init_modal([0,360],[0,360,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,360,self.rotate_mod_angle,1)
		if self.modal_window.exec_():
			self.rotate_mod_angle = self.modal_window.button_confirm_exit()
		self.auto_rotate_exec()

	def auto_resize_exec(self):
		self.set_sizes(self.image.resize((int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1]))))
		self.loadImageFromPIX(self.image.resize((int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1]))))

	def auto_resize(self):
		self.modal_window = Modal("Zmiana rozmiaru")
		self.modal_window.init_resize_modal(["Wysokość (pix)", "Szerokość (pix)"])
		if self.modal_window.exec_():
			self.resize_mod_dim = self.modal_window.button_nonsignal_confirm_exit()
		self.auto_resize_exec()

	def auto_new_exec(self):
		self.image = Image.new("RGBA",(int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1])),(255,255,255,255))
		self.set_sizes(self.image)
		self.loadImageFromPIX(self.image)

	def	auto_new(self):
		self.modal_window = Modal("Wymiary nowego pliku")
		self.modal_window.init_resize_modal(["Wysokość (pix)", "Szerokość (pix)"])
		if self.modal_window.exec_():
			self.resize_mod_dim = self.modal_window.button_nonsignal_confirm_exit()
		self.auto_new_exec()
		
	def auto_brightness_exec(self):
		self.enhancer = ImageEnhance.Brightness(self.image)			
		self.image = self.enhancer.enhance(self.brightness_mod_value/100)
		self.loadImageFromPIX(self.image)

	def auto_brightness(self):
		self.modal_window = Modal("Zmiana jasności","Jasność (%): ")
		self.modal_window.init_modal([0,200],[0,200,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,200,self.brightness_mod_value,1)
		if self.modal_window.exec_():
			self.brightness_mod_value = self.modal_window.button_confirm_exit()
		self.auto_brightness_exec()
		
	#mialo byc usuniete
	def auto_colorbalance(self):
		self.modal_window = Modal("Balans kolorów","Stopień balansu (%): ")
		self.modal_window.init_modal([0,200],[0,200,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,200,self.colbalance_mod_value,1)
		if self.modal_window.exec_():
			self.enhancer = ImageEnhance.Color(self.image)
			self.colbalance_mod_value = self.modal_window.button_confirm_exit()
			self.image = self.enhancer.enhance(self.colbalance_mod_value/100)
		self.loadImageFromPIX(self.image)

	def auto_filter(self, selected_filter):
		self.image = self.image.filter(selected_filter)
		self.loadImageFromPIX(self.image)

	def auto_add_text_exec(self,txt,text_color):
		self.font = PIL.ImageFont.truetype("arial.ttf", 15)
		self.drawer = PIL.ImageDraw.Draw(txt)
		self.drawer.text((self.mouse_pos[0],self.mouse_pos[1]), self.input_text, font=self.font, fill= text_color)
		tmp_out = Image.alpha_composite(self.image, txt)
		self.image = tmp_out
		self.loadImageFromPIX(self.image)

	def auto_add_text(self):
		self.modal_window = Modal("Wprowadź tekst do wstawienia ")
		self.modal_window.init_text_modal()
		if self.modal_window.exec_():
			txt = Image.new('RGBA', self.image.size, (255,255,255,255))

			self.input_text = self.modal_window.button_nonsignal_confirm_exit("text")
		text_color = self.modal_window.init_color_picker("Kolor tekstu")
		self.auto_add_text_exec(txt,text_color)
		

	def auto_gaussianblur_exec(self):
		self.image = self.image.filter(ImageFilter.GaussianBlur(self.gaussian_radius))
		self.loadImageFromPIX(self.image)

	def auto_gaussianblur(self):
		self.modal_window = Modal("Rozmycie Gaussa","Promień rozmycia: ")
		self.modal_window.init_modal([0,10],[0,10,1])
		self.modal_window.set_slider(self.modal_window.get_slider(), 0,10,self.gaussian_radius,10)
		if self.modal_window.exec_():
			self.gaussian_radius  = self.modal_window.button_confirm_exit()
		self.auto_gaussianblur_exec()

	def auto_unsharpmask_exec(self, value_changed):
		if value_changed:
			unsharp_img =self.image.filter(ImageFilter.UnsharpMask(self.unsharp_mod_values[0],self.unsharp_mod_values[1],self.unsharp_mod_values[2]))
			self.image = unsharp_img
			self.loadImageFromPIX(self.image)

	def auto_unsharpmask(self):
		value_changed = False
		self.modal_window = Modal("Maska wyostrzająca")
		self.modal_window.init_unsharp_mask()
		self.modal_window.set_sliders(self.modal_window.get_sliders(), self.unsharp_mod_values)
		if self.modal_window.exec_():
			self.unsharp_mod_values  = self.modal_window.button_confirm_exit()
			value_changed = True
		self.auto_unsharpmask_exec(value_changed)

	def auto_kernel(self,size):
		self.modal_window = Modal("Zdefiniuj maskę")
		self.modal_window.init_own_mask_modal(size)
		if self.modal_window.exec_():
			self.kernel_vals  = self.modal_window.button_nonsignal_confirm_exit("unsharp")
			kernel_img = self.image.filter(ImageFilter.Kernel(self.kernel_vals[0], self.kernel_vals[1]))
		self.image = kernel_img
		self.loadImageFromPIX(self.image)

	def auto_rankfilter_exec(self):
		rank_img = self.image.filter(ImageFilter.RankFilter(self.rankfilter_size,int(self.rankfilter_size*self.rankfilter_size/2)))
		self.image = rank_img
		self.loadImageFromPIX(self.image)

	def auto_rankfilter(self):
		self.modal_window = Modal("Filtr rankingowy","Rozmiar rozmycia: ")
		self.modal_window.init_modal([1,15],[1,15,2])
		self.modal_window.set_slider(self.modal_window.get_slider(), 1,15,self.rankfilter_size,2)
		if self.modal_window.exec_():
			self.rankfilter_size  = self.modal_window.button_confirm_exit()
		self.auto_rankfilter_exec()

# TUTAJ PORPAWIC +++++++++++++++++++++++++++++++++++++++++++++++++
	def auto_medianfilter_exec(self):
		median_img = self.image.filter(ImageFilter.MedianFilter(self.medianfilter_size))
		self.image = median_img
		self.loadImageFromPIX(self.image)

	def auto_medianfilter(self):
		self.modal_window = Modal("Filtr medianowy","Rozmiar rozmycia: ")
		self.modal_window.init_modal([1,15],[1,15,2])
		self.modal_window.set_slider(self.modal_window.get_slider(),1,15,self.medianfilter_size,2)
		if self.modal_window.exec_():
			self.medianfilter_size  = self.modal_window.button_confirm_exit()
		self.auto_medianfilter_exec()

	def auto_minfilter_exec(self):
		minfilter_img = self.image.filter(ImageFilter.MinFilter(self.minfilter_size))
		self.image = minfilter_img
		self.loadImageFromPIX(self.image)
		
	def auto_minfilter(self):
		self.modal_window = Modal("Filtr minimalny","Rozmiar rozmycia: ")
		self.modal_window.init_modal([1,15],[1,15,2])
		self.modal_window.set_slider(self.modal_window.get_slider(),1,15,self.minfilter_size,2)
		if self.modal_window.exec_():
			self.minfilter_size  = self.modal_window.button_confirm_exit()
		self.auto_minfilter_exec()
		
	def auto_maxfilter_exec(self):
		maxfilter_img = self.image.filter(ImageFilter.MaxFilter(self.maxfilter_size))
		self.image = maxfilter_img
		self.loadImageFromPIX(self.image)

	def auto_maxfilter(self):
		self.modal_window = Modal("Filtr maksymalny","Rozmiar rozmycia: ")
		self.modal_window.init_modal([1,15],[1,15,2])
		self.modal_window.set_slider(self.modal_window.get_slider(),1,15,self.maxfilter_size,2)
		if self.modal_window.exec_():
			self.maxfilter_size  = self.modal_window.button_confirm_exit()
		self.auto_maxfilter_exec()
		
	def auto_modefilter_exec(self):
		modalfilter_img =self.image.filter(ImageFilter.ModeFilter(self.modalfilter_size))
		self.image = modalfilter_img
		self.loadImageFromPIX(self.image)

	def auto_modefilter(self):
		self.modal_window = Modal("Filtr modalny", "Rozmiar rozmycia: ")
		self.modal_window.init_modal([0,10],[0,10,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,10,self.modalfilter_size,10)
		if self.modal_window.exec_():
			self.modalfilter_size  = self.modal_window.button_confirm_exit()
		self.auto_modefilter_exec()

	def pre_treshold(self):
		self.modal_window = Modal("Progowanie", "Próg: ")
		self.modal_window.init_modal([0,255],[0,255,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,255,self.treshold_value,1)
		if self.modal_window.exec_():
			self.treshold_value = self.modal_window.button_confirm_exit()
		self.treshold(self.treshold_value)
		

	def treshold(self, value):
		copy = self.image.copy()
		tup_value = (value,value,value)
		white = (255,255,255)
		black = (0,0,0)
		for w in range(self.width):
			for h in range(self.height):
				color = self.image.getpixel((w,h))
				red, green, blue = color
				red_lim, green_lim, blue_lim = tup_value
				if((red>red_lim) and (green>green_lim) and (blue>blue_lim)):
					copy.putpixel((w,h),white)
				else:
					copy.putpixel((w,h),black)
		self.image = copy
		self.loadImageFromPIX(self.image)

	def saturation_exec(self):
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

	def saturation(self):
		self.modal_window = Modal("Nasycenie","Stopień nasycenia (%): ")
		self.modal_window.init_modal([0,200],[0,200,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,200,self.saturation_mod_value,1)
		if self.modal_window.exec_():
			self.saturation_mod_value = self.modal_window.button_confirm_exit()
		self.saturation_exec()
		
 
	def gamma_correction_exec(self):
		in_data = numpy.asarray(self.image, dtype=numpy.uint8)
		in_data = in_data/255.
		in_data = in_data ** self.gamma_mod_value
		in_data = in_data*255.9999
		in_data = numpy.uint8(in_data)
		self.image = Image.fromarray(in_data)
		self.loadImageFromPIX(self.image)

	def gamma_correction(self):
		self.modal_window = Modal("Korekcja Gamma", "Wartość wspołczynnika: ")
		self.modal_window.init_modal([0.01,7.99],[0.01,7.99,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),1,799,self.gamma_mod_value,1)
		if self.modal_window.exec_():
			self.gamma_mod_value = 1.0/(self.modal_window.button_confirm_exit()/100.0)
		self.gamma_correction_exec()
		
 
	def color_change_exec(self):
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

	def color_change(self):
		self.modal_window = Modal("Koło barw", "Zmiana koloru (%): ")
		self.modal_window.init_modal([0,360],[0,360,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,360,self.color_mod_value,1)
		if self.modal_window.exec_():
			self.color_mod_value = self.modal_window.button_confirm_exit()
		self.color_change_exec()

	def noise_generator_exec(self):
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
 
	def noise_generator(self):
		self.modal_window = Modal("Pieprz i sol", "Zaszumienie (%): ")
		self.modal_window.init_modal([0,100],[0,100,1])
		self.modal_window.set_slider(self.modal_window.get_slider(),0,100,self.noise_mod_value,1)
		if self.modal_window.exec_():
			self.noise_mod_value = self.modal_window.button_confirm_exit()
		self.noise_generator_exec()
		

	def sample_color(self):
		if self.mouse_pos[0] <= self.width and self.mouse_pos[1] <= self.height:
			pix = self.image.getpixel((self.mouse_pos[0],self.mouse_pos[1]))
			self.modal_window = Modal("Wartość koloru (RGB)")
			self.modal_window.init_color_sampler(pix)
			self.modal_window.exec_()

	def get_hist(self):
		self.hist = Histogram(self.image)
		self.hist.create_histogram()
		self.hist.draw_histogram()

	def show_histogram(self):
		self.get_hist()
		self.modal_window = Modal("Histogram")
		self.modal_window.init_histogram_drawer(self.hist.get_hist_img());
		self.modal_window.exec_()

	def put_marker_exec(self):
			# print(self.marker_mod_values)
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

	def put_marker(self):
		self.modal_window = Modal("Wstawianie markera")
		self.modal_window.init_markers_modal()
		if self.modal_window.exec_():
			self.marker_mod_values = self.modal_window.button_nonsignal_confirm_exit("marker")
		self.put_marker_exec()
		

	def auto_clipping(self, clip_pos):
		print(tuple(clip_pos))
		cropped_img = self.image.crop(tuple(clip_pos))
		self.set_sizes(cropped_img)
		self.image = cropped_img
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
